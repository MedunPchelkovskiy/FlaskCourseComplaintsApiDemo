# from cloudinary.templatetags import cloudinary
# from flask import request
# from flask_restful import Resource
#
# from helpers.decorators import permission_required
# from managers.authentication import auth
# from models import RoleType
#
#
# class FileResource(Resource):
#     @auth.login_required
#     @permission_required(RoleType.complainer)
#     def post(self):
#         file = request.files['file']
#         if not file:
#             return 'Please select file'
#         image =
#
#
#         upload_result = cloudinary.uploader.upload(file)
#         app.logger.info(upload_result)
#         return jsonify(upload_result)
#         # file.save('/uploads' + file.filename)
#         # return 'File uploaded successfully!'
