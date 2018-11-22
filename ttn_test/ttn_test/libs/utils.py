from flask import Flask, Response
import json

#from app import logger
from bson import json_util


def ErrorResponse(error):
	return Response(json.dumps({ 'status' : False, 'message' : error }), mimetype="application/json")


def SuccessResponse(response):
	response['status'] = True
	return Response(json.dumps(response, default=json_util.default ), mimetype="application/json")


def Exception(exception):
	return {
		'status' : False,
		'message' : ("Error: %s" % exception)
	}