from langgraph.graph import StateGraph, END
from domain import EmbeddingModel, DocumentStore, RAGResult, RAGWorkFlow
from typing import Any, Dict
from application import MAX_CONTEXT_CHARS

#Orchestrator RAG System
class LangGraphRAG(RAGWorkFlow):
    #Encapsulates the RAG (Retrieve -> Answer) workflow.
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        document_store: DocumentStore,
        max_content_chars: int = MAX_CONTEXT_CHARS

    ):
        self._embedding_model = embedding_model
        self._document_store = document_store
        self._max_content_chars = max_content_chars
        self._chain = self._build_workflow()
   
    #Build and compile LangGraph workflow
    def _build_workflow(self) -> Any:
        #set empty LangGraph state as dictionary
        workflow = StateGraph(dict)
        
        #add retrieve and answer node to graph
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("answer", self._answer_node)

        #set entry point and exit
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)

        return workflow.compile()

    def _answer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        context = state.get("context", [])

        if context:
            preview = context[0].text[:100]
            answer = f"I found this: '{preview}...'"
        else:
            answer = "Sorry, I don't know."

        state["answer"] = answer
        return state

    def _retrieve_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        query = state["question"]
        query_embedding = self._embedding_model.embed(query)
        
        results = self._document_store.search(
            query_embedding=query_embedding,
            limit=2,
            query_text=query
        )

        state["context"] = results
        return state
    def invoke(self, question: str) -> RAGResult:


        result = self._chain.invoke({"question": question})

        return RAGResult(
            question=question,
            answer=result["answer"],
            context=result.get("context", [])
        )

    @property
    def is_ready(self) -> bool:
        return self._chain is not None
