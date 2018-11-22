from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.colors import PCMYKColor
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets.markers import makeMarker

from datetime import datetime

import pymongo
from pymongo import MongoClient
client = MongoClient()#'mongodb://gpstracking:droidhomes@localhost:27017')
db = client.user
from bson.objectid import ObjectId
timeformat = '%Y-%m-%d %H:%M:%S'

class DataToPdf():
	def __init__(self, fields, data, title=None):
		self.fields = fields
		self.data = data
		self.title = title

	def export(self, filename, data_align='LEFT', table_halign='LEFT'):
		doc = SimpleDocTemplate(filename, pagesize=letter)
		styles = getSampleStyleSheet()
		styleH = styles['Heading1']
		story = []
		if self.title:
			story.append(Paragraph(self.title, styleH))
			story.append(Spacer(1, 0.25 * inch))

		converted_data = self.__convert_data()
		table = Table(converted_data, hAlign=table_halign)
		table.setStyle(TableStyle([
			('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
			('ALIGN', (0, 0), (-1, 0), 'CENTER'),
			('ALIGN',(0, 0),(0,-1), data_align),
			('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
			('BOX', (0,0), (-1,-1), 0.25, colors.black),
		]))

		story.append(table)
		doc.build(story)

	def __convert_data(self):
		keys, names = zip(*[[k, n] for k, n in self.fields])
		new_data = [names]
		for d in self.data:
			new_data.append([d[k] for k in keys])
		return new_data


class hbpdfbuilder():
	def __init__(self,name,id,intime,outtime,modelResponse ,title=None):
		self.title = title
		self.name= name
		self.id = id
		self.intime = intime
		self.outtime = outtime
		self.modelResponse=modelResponse
		

	def export(self, filename, data_align='LEFT', table_halign='LEFT'):
		doc = SimpleDocTemplate(filename, #pagesize=letter,
									rightMargin=30, leftMargin=30, topMargin=30,
				bottomMargin=20)
		styles = getSampleStyleSheet()
		styleH = styles['Heading1']
		story = []
		if self.title:
			story.append(Paragraph(self.title, styleH,))
			story.append(Spacer(1, 0.25 * inch))
			story.append(Paragraph(self.name, styles['Normal']))


		headings = ( 'Intime', 'Outtime')
		data = [(p['intime'], p['outtime']) for p in self.modelResponse]
		table = Table([headings] + data)
		table.setStyle(TableStyle(
			[
				('GRID', (0, 0), (5, -1), 1, colors.dodgerblue),
				('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
			]
		))
		story.append(table)
		doc.build(story)
