import json
from typing import Any

def rerank_documents(bedrock_client: Any, model_id: str, query: str, documents: list[dict[str, Any]], top_n: int = 5) -> list[dict[str, Any]]:
    """Reranks documents based on relevance to a query using AWS Bedrock's reranking model.

    Args:
        bedrock_client: Authenticated AWS Bedrock runtime client
        model_id: Identifier of the Bedrock reranking model (e.g., 'cohere-rerank-model')
        query: Search query text to use for relevance scoring
        documents: List of document dictionaries to rerank. Each document must contain:
                  - 'content': Text content of the document
                  - [other fields]: Any additional metadata to preserve
        top_n: Maximum number of documents to return (default: 5)

    Returns:
        List of document dictionaries sorted by relevance score, each enhanced with:
        - 'relevance_score': Numerical score indicating match quality (higher is better)
        - All original document fields preserved

    Notes:
        - Returns documents in original order if reranking fails
        - Maintains all original document metadata in the output
        - Uses Cohere's reranking model through Bedrock API

    Example:
        >>> docs = [{'content': 'cat food', 'id': 1}, {'content': 'dog food', 'id': 2}]
        >>> rerank_documents(client, 'cohere-rerank', 'pet nutrition', docs, top_n=2)
        [
            {'content': 'dog food', 'id': 2, 'relevance_score': 0.92},
            {'content': 'cat food', 'id': 1, 'relevance_score': 0.85}
        ]
    """
    try:
        # Prepare documents for reranking
        doc_texts = [doc['content'] for doc in documents]
        
        # Call Cohere Rerank model
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps({
                "query": query,
                "documents": doc_texts,
                "top_n": top_n,
                "return_documents": True
            }),
            contentType="application/json"
        )
        
        # Parse response
        result = json.loads(response['body'].read())
        
        # Map back to original documents with scores
        reranked_docs = []
        for item in result['results']:
            original_doc = documents[item['index']]
            reranked_docs.append({
                **original_doc,
                'relevance_score': item['relevance_score']
            })
        
        return reranked_docs[:top_n]
    
    except Exception as e:
        print(f"Error in reranking: {str(e)}")
        return documents[:top_n]  # Fallback to original order if reranking fails

def retrieve_rerank_context_from_opensearch(
    bedrock_client: Any,
    model_id: str,
    opensearch_client: Any,
    opensearch_index_name: str,
    embed_model: Any,
    query: str,
    top_k: int = 15,
    rerank_top_n: int = 5
) -> str:
    """Retrieves and reranks relevant context from OpenSearch using vector search and LLM reranking.

    Performs a two-stage retrieval process:
    1. Initial vector similarity search in OpenSearch
    2. Semantic reranking of results using an LLM model

    Args:
        bedrock_client: Authenticated AWS Bedrock runtime client
        model_id: Model id for rerank
        opensearch_client: Authenticated OpenSearch client
        opensearch_index_name: Name of the OpenSearch index to query
        embed_model: Embedding model instance with get_text_embedding() method
        query: Search query string
        top_k: Number of initial documents to retrieve from OpenSearch (default: 15)
        rerank_top_n: Number of top documents to return after reranking (default: 5)

    Returns:
        str: Formatted context string containing the top documents with metadata, or empty string on error

    Notes:
        - Documents must have 'content' and 'filename' fields in OpenSearch
        - First stage uses k-NN vector search
        - Second stage uses semantic reranking
        - Returns empty string if any step fails

    Example:
        >>> context = retrieve_rerank_context_from_opensearch(
                bedrock_client,
                opensearch_client,
                "knowledge-base",
                embed_model,
                "What is machine learning?",
                top_k=10,
                rerank_top_n=3
            )
        >>> print(context)
        Fonte: ml_intro.pdf
        Conteúdo: Machine learning is a subset of AI...
        Score: 0.92
        ...
    """
    try:
        # Generate embedding for the query
        query_embedding = embed_model.get_text_embedding(query)
        
        # Initial vector search (get more results than needed for reranking)
        search_body = {
            "size": top_k,
            "query": {
                "knn": {
                    "vector": {
                        "vector": query_embedding,
                        "k": top_k
                    }
                }
            },
            "_source": ["content", "filename"]
        }
        
        response = opensearch_client.search(
            index=opensearch_index_name,
            body=search_body
        )
        
        # Extract documents for reranking
        documents = [
            {
                "content": hit["_source"]["content"],
                "filename": hit["_source"]["filename"],
                "score": hit["_score"]
            }
            for hit in response['hits']['hits']
        ]
        
        # Rerank documents
        reranked_docs = rerank_documents(bedrock_client, model_id, query, documents, top_n=rerank_top_n)
        
        # Format final context
        contexts = []
        for doc in reranked_docs:
            contexts.append(
                f"Fonte: {doc['filename']}\n"
                f"Conteúdo: {doc['content']}\n"
                f"Score: {doc.get('relevance_score', doc['score']):.2f}\n"
            )
        
        return "\n".join(contexts)
    
    except Exception as e:
        print(f"Error retrieving context: {str(e)}")
        return ""