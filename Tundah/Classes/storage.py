from qdrant_client import QdrantClient, models

from qdrant_client.models import Distance, VectorParams, PointStruct

class Storage:

    def __init__(self):

        self.client = QdrantClient(url="http://localhost:6333")
        self.collection_name="server_documents"
        
        # Check if the collection exists
        if not self.client.collection_exists(collection_name=self.collection_name):
            print(f"Collection '{self.collection_name}' does not exist. Creating it now.")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.DOT),
            )

    def insert_to_qdriant(self, vectors, meta_data):
        # Insert data
        print("Insertion into Vector DATA Base...")
        for index, row in enumerate( zip(vectors, meta_data) ):
            self.client.upsert(
                collection_name=self.collection_name,
                wait=True,
                points=[
                    PointStruct(id=index, vector=row[0], payload=row[1]),
                ],
            )
            
    
    # To search for simmilar points based on a vector
    def search_documents(self, query_vector, limit=3):

        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            with_vectors=True,
            with_payload=True,
            limit=limit,
        )
    
    # To count all points in a collection
    def count_all_points(self):
        count = 0
        for _ in self.client.scroll(collection_name=self.collection_name, limit=10000):
            count += 1
        print(f"Total points in collection {self.collection_name}: {count}")
        return count

    # To delete a specific point from a Qdrant collection
    def delete_point_by_condition(self, key, value):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value),
                        ),
                    ],
                )
            ),
        )
        print(f"Deleted points where {key} is {value} in collection {self.collection_name}.")

            
    

