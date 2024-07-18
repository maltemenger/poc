# 1.Setup
- Install pipenv
- Install dependencies

## 1.1 Add Datasources
- create folder --> .data
- add pdfs --> g1.pdf
- add pdf --> netznutzungsvertrag.pdf

## 1.2 Start Flask-App
- flask --app main --debug run

## 1.3 Vectorize data 
- Load postman.json into postman
- execute post initialize_data from postman

## 1.4 Execute Tests
- Execute tests in postman: test multiple expectations

payload example:
[
        {
    "question": "Welche Schalter und Drehtaster im G1 sind verplombt?",
    "expectations": [
        {
            "pages": [47],
            "source_doc": "g1.pdf"
    }
    ]
   }
]
