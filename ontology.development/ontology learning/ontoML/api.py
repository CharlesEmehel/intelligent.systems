from flask import Blueprint, jsonify, request
from .models import db, Item

api_bp = Blueprint('api', __name__)

@api_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [{"id": item.id, "entityname": item.entityname, "type": item.type} for item in items]
    return jsonify(items_list)

@api_bp.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    item_data = {"id": item.id, "entityname": item.entityname, "type": item.type}
    return jsonify(item_data)
