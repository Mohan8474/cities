from flask import Blueprint, request, current_app, url_for
from app.models import Cities, CitiesSchema
from app import db
from sqlalchemy import desc


cities_api = Blueprint("cities_api", __name__, url_prefix="/cities")
cities_schema = CitiesSchema(many=True)


class CitiesException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


@cities_api.errorhandler(CitiesException)
def handle_exception(e):
    current_app.logger.exception(e)
    return {"success": False, "error": e.message}, e.code


@cities_api.route("/", methods=["GET"])
@cities_api.route("/<int:id>", methods=["GET"])
def get_cities(id=None):
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 5, type=int)
    order = request.args.get("order", "asc")
    sort = request.args.get("sort", "area")
    search = request.args.get("search")

    city = Cities.query

    if id:
        city = city.filter(Cities.id == id)
        if not city.first():
            raise CitiesException(
                f"Cities with id {id} doesn't exist.",
                404,
            )

    if order == "asc":
        city = city.order_by(sort)
    else:
        city = city.order_by(desc(sort))

    if search:
        city = city.filter(Cities.name.ilike(f"%{search}%"))

    city = city.paginate(page=page, per_page=limit, error_out=False)

    all_cities = cities_schema.dump(city)
    if len(all_cities) == 0:
        raise CitiesException(
            "No city found.",
            404,
        )

    if city.has_next:
        next_url = url_for("cities_api.get_cities", page=city.next_num)
    else:
        next_url = None

    return {
        "all_pokemon": all_cities,
        "total": city.total,
        "order": order,
        "sort": sort,
        "page": city.page,
        "total_pages": city.pages,
        "next_page": next_url,
    }, 200


@cities_api.route("/", methods=["POST"])
def add_cities():
    for cities in request.get_json():
        country = cities.get("country")
        name = cities.get("name")
        lat = cities.get("lat")
        lng = cities.get("lng")
        area = cities.get("area")

        new_city = Cities(country=country, name=name, lat=lat, lng=lng, area=area)
        db.session.add(new_city)
    db.session.commit()

    return {"msg": "City Added Succesfully"}


@cities_api.route("/", methods=["DELETE"])
@cities_api.route("/<int:id>", methods=["DELETE"])
def delete_cities(id=None):
    """
    This API deletes the cities.
    Deletes single city if id is passed else deletes all city
    """
    if id:
        city = Cities.query.get(id)
        if city is None:
            raise CitiesException("No Data Exists", 404)
        db.session.delete(city)
    else:
        db.session.query(Cities).delete()
        db.session.commit()

    db.session.commit()
    return {"message": "Successfully deleted"}, 200
