from flask import Blueprint, request, jsonify, abort
from app import db
from app.models import Note

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


@notes_bp.route("", methods=["POST"])
def create_note():
    """
    Создание заметки:
    POST /notes
    Тело JSON:
    {
      "title": "Заголовок заметки",
      "content": "Текст заметки"
    }
    """
    data = request.get_json()
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Bad Request: title and content required"}), 400

    title = data["title"]
    content = data["content"]
    note = Note(title=title, content=content)
    db.session.add(note)
    db.session.commit()
    return jsonify({"id": note.id}), 201


@notes_bp.route("", methods=["GET"])
def get_all_notes():
    """
    Получение всех заметок:
    GET /notes
    Ответ: список заметок
    """
    notes = Note.query.all()
    return jsonify([note.to_dict() for note in notes]), 200


@notes_bp.route("/<int:note_id>", methods=["GET"])
def get_note_by_id(note_id):
    """
    Получение заметки по ID:
    GET /notes/<id>
    """
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict()), 200


@notes_bp.route("/<int:note_id>", methods=["DELETE"])
def delete_note_by_id(note_id):
    """
    Удаление заметки по ID:
    DELETE /notes/<id>
    """
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return "", 204
