from langgraph.graph import StateGraph, END
from domain import EmbeddingModel, DocumentStore, Document, RAGWorkFlow
from typing import Any, Dict
from application import MAX_CONTEXT_CHARS

#Orchestrator RAG System
class LangGraphRAG(RAGWorkFlow):
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        document_store: DocumentStore,
        max_content_chars: MAX_CONTEXT_CHARS

    ):
        self._embedding_model = embedding_model
        self._document_store = document_store
        self._max_content_chars = max_content_chars
        self._chain = self._build_workflow()
   
    #Build graph
    def _build_workflow(self) -> Any:
        
        workflow = StateGraph(dict)
        
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("answer", self._answer_node)

        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)

        return workflow.compile()

    def _answer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:

        context = state.get("context", [])


        if context:
            preview = context[0].text[:self._max_context_chars]  # Document has .text
            answer = f'I found this: "{preview}..."'

        else:
            answer = "I don't know."

        state["answer"] = answer
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
