import os
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_handler import chroma_conf
from model.factory import embed_model
from utils.path_tool import get_abs_path
from utils.file_handler import get_file_md5_hex,listdir_with_allowed_type,pdf_loader,text_loader
from utils.logger_handler import logger

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name = chroma_conf["collection_name"],
            embedding_function = embed_model,
            persist_directory = chroma_conf["persist_directory"],
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = chroma_conf["chunk_size"],
            chunk_overlap = chroma_conf["chunk_overlap"],
            separators = chroma_conf["separators"],
            length_function = len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_documents(self):
        '''
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的MD5，做去重
        '''
        def check_md5_hex(md5_for_check:str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]),"w",encoding="utf-8").close()
                return False
            
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"r",encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True   #MD5处理过
                
                return False    #MD5未处理过
        
        def save_md5_hex(md5_for_check:str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]),"a",encoding="utf-8") as f:
                f.write(md5_for_check+"\n")

        def get_file_documents(read_path:str):
            if read_path.endswith("txt"):
                return text_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)
            
            return []

        allowed_files_path:list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"])
        )
        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[load_documents]文件{path}的内容已存在知识库内，跳过")
                continue
            try:
                documents:list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[load_documents]文件{path}没有有效文本内容，跳过")
                    continue

                split_documents:list[Document] = self.splitter.split_documents(documents)

                if not split_documents:
                    logger.warning(f"[load_documents]文件{path}分片后没有有效文本内容，跳过")
                    continue

                self.vector_store.add_documents(split_documents)
                save_md5_hex(md5_hex)
                logger.info(f"[load_documents]文件{path}的内容已成功存入知识库")
            except Exception as e:
                logger.error(f"[load_documents]文件{path}的内容存入知识库失败: {str(e)}",exc_info=True)
                continue

if __name__ == "__main__":
    vector_store_service = VectorStoreService()
    vector_store_service.load_documents()
    retriever = vector_store_service.get_retriever()
    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)


