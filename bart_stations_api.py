from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.postgresConn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abbr = db.Column(db.String(255))
    name = db.Column(db.String(50))
    gtfs_latitude = db.Column(db.String(255))
    gtfs_longitude = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(500))
    county = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zipcode = db.Column(db.String(255))


    def __repr__(self):
        return '<Station %s>' % self.name
    
class StationSchema(ma.Schema):
    class Meta:
        fields = ("id", "abbr", "name", "gtfs_latitude", "gtfs_longitude", "address", "city", "county", "state", "zipcode")

station_schema = StationSchema()
stations_schema = StationSchema(many=True)

class StationListResource(Resource):
    def get(self):
        stations = Station.query.all()
        return stations_schema.dump(stations)

    def post(self):
        new_station = Station(
            abbr=request.json['abbr'],
            name=request.json['name'],
            gtfs_latitude=request.json['gtfs_latitude'],
            gtfs_longitude=request.json['gtfs_longitude'],
            address=request.json['address'],
            city=request.json['city'],
            county=request.json['county'],
            state=request.json['state'],
            zipcode=request.json['zipcode'],
        )
        db.session.add(new_station)
        db.session.commit()
        return station_schema.dump(new_station)

class StationResource(Resource):
    def get(self, station_id):
        station = Station.query.get_or_404(station_id)
        return station_schema.dump(station)

    def patch(self, station_id):
        station = Station.query.get_or_404(station_id)

        if 'abbr' in request.json:
            station.abbr = request.json['abbr']
        if 'name' in request.json:
            station.name = request.json['name']
        if 'gtfs_latitude' in request.json:
            station.gtfs_latitude = request.json['gtfs_latitude']
        if 'gtfs_longitude' in request.json:
            station.gtfs_longitude = request.json['gtfs_longitude']
        if 'address' in request.json:
            station.address = request.json['address']
        if 'city' in request.json:
            station.city = request.json['city']
        if 'county' in request.json:
            station.county = request.json['county']
        if 'state' in request.json:
            station.state = request.json['state']
        if 'zipcode' in request.json:
            station.zipcode = request.json['zipcode']
            
        db.session.commit()
        return station_schema.dump(station)

    def delete(self, station_id):
        station = Station.query.get_or_404(station_id)
        db.session.delete(station)
        db.session.commit()
        return '', 204

api.add_resource(StationListResource, '/stations/')
api.add_resource(StationResource, '/stations/<int:station_id>/')

if __name__ == '__main__':
    app.run(debug=True)
