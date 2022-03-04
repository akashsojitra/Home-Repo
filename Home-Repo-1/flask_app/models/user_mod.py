from flask import flash
import re
from flask_app import app
from flask_app.models import listing_mod
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class Users:
    db_name = "homelisting"
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.createdDate = data['createdDate']
        self.updatedDate = data['updatedDate']
        self.listings = []

    @staticmethod
    def validate_register(user):
        is_valid = True
        users_with_email = Users.get_by_email({'email': user['email']})
        if users_with_email:
            flash("There is already an account associated with this email.")
            is_valid = False
        if len(user['firstName']) < 2:
            flash("Please provide a first name.")
            is_valid = False
        if len(user['lastName']) < 2:
            flash("Please provide a last name.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must have more than 8 characters.")
            is_valid = False
        if (user['password']) != (user['r_password']):
            flash("Repeated passwords must match!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        users_with_email = Users.get_by_email({'email': user['email']})
        if not users_with_email:
            flash("Invalid Email/Password. Please Try Again.")
            is_valid = False
        if users_with_email:
            if len(user['email']) < 8:
                flash("Invalid Email/Password. Please Try Again.")
                is_valid = False
            if len(user['password']) < 8:
                flash("Invalid Email/Password. Please Try Again.")
                is_valid = False
        return is_valid

    @classmethod
    def get_profile(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if not results:
            return False
        one_user = cls(results[0])
        return one_user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (firstName, lastName, email, password, createdDate, updatedDate) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET firstName=%(firstName)s, lastName=%(lastName)s, updated_at=NOW() WHERE id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def user_listings(cls, data):
        query = "select * from users left join listings on users.id = listings.userId WHERE users.id = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        user = cls(result[0])
        for db_row in result:
            data = {
                'id': db_row['listings.id'],
                'title': db_row['title'],
                'description': db_row['description'],
                'listPrice': db_row['listPrice'],
                'imgURL': db_row['imgURL'],
                'createdDate': db_row['createdDate'],
                'updatedDate': db_row['updatedDate'],
                'userId' : db_row['userId']
            }
            temp = listing_mod.Listings(data)
            user.listings.append(temp)
        return user