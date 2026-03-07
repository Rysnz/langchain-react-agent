from abc import ABC,abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.chat_models.tongyi import BaseChatModel
from utils.config_handler import rag_conf

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[BaseChatModel|Embeddings]:
        pass
    
class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[BaseChatModel|Embeddings]:
        return ChatTongyi(model=rag_conf["chat_model_name"])
        
class EmbeddingModelFactory(BaseModelFactory):
    def generator(self) -> Optional[BaseChatModel|Embeddings]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingModelFactory().generator()
        