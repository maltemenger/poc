def are_all_expectations_met(similarity_chunks, expectation):
    expected_source_doc = expectation['source_doc']
    expected_pages = expectation['pages']

    filtered_chunks_by_expected_document = list(filter(lambda chunk: chunk.source_doc == "data/"+expected_source_doc, similarity_chunks))
    return all(page in [doc.page for doc in filtered_chunks_by_expected_document] for page in expected_pages)


def build_expecation_test_response(similariy_chunks, all_expectations_met):
    docs_with_test_result = []
    for doc in similariy_chunks:
        obj_dict = doc.__dict__
        docs_with_test_result.append(obj_dict)

    return {
        'allExpectationsMet': all_expectations_met,
        'objects': docs_with_test_result
    }