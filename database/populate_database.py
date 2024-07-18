from services.chroma_service import ChromaService

newChroma = ChromaService()
newChroma.add_document('../data/g1.pdf', 'g1')

newChroma = ChromaService()
newChroma.add_document('../data/netznutzungsvertrag.pdf', 'netz')
