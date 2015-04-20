# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

import re

import logging
_logger = logging.getLogger(__name__)



from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

        
class website_project(http.Controller):

    # get blog posts where both year and tag (string) matches
    def get_posts(self,tag,year):
        return request.env['blog.tag'].search([('name','=',tag)])[0].post_ids.filtered(lambda p: year.id in [y.id for y in p.tag_ids] ).sorted(lambda p: p.sequence) 
        # use foreach get_posts('elevhalsa',year) as post
    
    # get project and indirect issues where both year and tag (string) matches
    def get_projects(self,tag,year):
        #tag_id = request.env['blog.tag'].search([('name','=',tag)])[0].id
        return request.env['project.project'].search(['&',('tag_ids','in',year.id),('tag_ids','in',request.env['blog.tag'].search([('name','=',tag)])[0].id)])
        # use foreach get_projects('elevhalsa',year) as project, foreach project.issue_ids as issue




    @http.route(['/rapport/<string:year>',], type='http', auth="public", website=True)
    def rapport(self, year=False, blog=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        year_obj = request.env['blog.tag'].search([('name','=',year)])[0]

        return request.website.render("project_blog_view.rapport", {
            'year': year_obj,
            'blog': blog,
            'self': self,
        })
        
        
class project_project(models.Model):
    _inherit = "project.project"

    tag_ids   = fields.Many2many('blog.tag',string="Blog Tags")
    
class blog_post(models.Model):
    _inherit = "blog.post"
    
    sequence = fields.Integer(default=50)
    
    
# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
