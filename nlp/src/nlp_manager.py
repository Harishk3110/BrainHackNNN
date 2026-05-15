"""Manages the NLP model."""

import math
import re


class NLPManager:
    STOPWORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "how",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "that",
        "the",
        "to",
        "was",
        "what",
        "when",
        "where",
        "which",
        "who",
        "why",
        "with",
    }

    def __init__(self):
        # This is where you can initialize your model and any static configurations.
        self.loaded = False
        self.documents: list[dict[str, str]] = []
        self.doc_tokens: dict[str, list[str]] = {}
        self.doc_freq: dict[str, int] = {}

    def load_corpus(self, documents: list[dict[str, str]]) -> None:
        """Loads the corpus of documents for RAG QA."""
        self.documents = documents
        self.doc_tokens = {}
        self.doc_freq = {}

        for document in documents:
            doc_id = document["id"]
            tokens = self._tokenize(document.get("document", ""))
            self.doc_tokens[doc_id] = tokens
            for token in set(tokens):
                self.doc_freq[token] = self.doc_freq.get(token, 0) + 1

        self.loaded = True

    def qa(self, question: str) -> dict[str, list[str] | str]:
        """Performs question answering on an image of a document.

        Args:
            question: The question to answer.

        Returns:
            A dictionary with two keys:
            - "documents": list of strings containing the most relevant document ids. Only the first 3 will be considered
            - "answer": string containing the answer to the question.
        """

        if not self.loaded or not self.documents:
            return {"documents": [], "answer": ""}

        question_tokens = self._tokenize(question)
        ranked_documents = self._rank_documents(question_tokens)
        if not ranked_documents or ranked_documents[0][0] <= 0:
            return {"documents": [], "answer": ""}

        top_ids = [doc_id for score, doc_id in ranked_documents if score > 0][:3]
        answer = self._best_answer_sentence(question_tokens, top_ids)

        return {"documents": top_ids, "answer": answer}

    def _tokenize(self, text: str) -> list[str]:
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        return [
            normalized
            for token in tokens
            if token not in self.STOPWORDS
            for normalized in [self._normalize_token(token)]
            if normalized
        ]

    def _normalize_token(self, token: str) -> str:
        if len(token) > 4 and token.endswith("ies"):
            return token[:-3] + "y"
        if len(token) > 5 and token.endswith("ing"):
            return token[:-3]
        if len(token) > 4 and token.endswith("ed"):
            return token[:-2]
        if len(token) > 4 and token.endswith("es"):
            return token[:-2]
        if len(token) > 3 and token.endswith("s"):
            return token[:-1]
        return token

    def _rank_documents(self, question_tokens: list[str]) -> list[tuple[float, str]]:
        if not question_tokens:
            return [(0.0, document["id"]) for document in self.documents]

        query_terms = set(question_tokens)
        total_docs = max(len(self.documents), 1)
        ranked = []
        for document in self.documents:
            doc_id = document["id"]
            tokens = self.doc_tokens.get(doc_id, [])
            if not tokens:
                ranked.append((0.0, doc_id))
                continue

            token_counts: dict[str, int] = {}
            for token in tokens:
                token_counts[token] = token_counts.get(token, 0) + 1

            score = 0.0
            for token in query_terms:
                count = token_counts.get(token, 0)
                if count == 0:
                    continue
                idf = math.log((1 + total_docs) / (1 + self.doc_freq.get(token, 0))) + 1
                score += (count / len(tokens)) * idf

            ranked.append((score, doc_id))

        ranked.sort(key=lambda item: (-item[0], item[1]))
        return ranked

    def _best_answer_sentence(self, question_tokens: list[str], doc_ids: list[str]) -> str:
        if not doc_ids:
            return ""

        documents_by_id = {document["id"]: document.get("document", "") for document in self.documents}
        query_terms = set(question_tokens)
        best_sentence = ""
        best_score = -1.0

        for doc_id in doc_ids:
            for sentence in self._split_sentences(documents_by_id.get(doc_id, "")):
                sentence_tokens = self._tokenize(sentence)
                if not sentence_tokens:
                    continue
                overlap = len(query_terms.intersection(sentence_tokens))
                score = overlap / math.sqrt(len(sentence_tokens))
                if score > best_score:
                    best_score = score
                    best_sentence = sentence

        return best_sentence[:300]

    def _split_sentences(self, text: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [sentence.strip() for sentence in sentences if sentence.strip()]
