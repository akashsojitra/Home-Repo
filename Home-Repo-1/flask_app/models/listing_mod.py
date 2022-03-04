from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_mod

class Listings:
    db_name = "homelisting"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.listPrice = data['listPrice']
        self.imgURL = data['imgURL']
        self.createDate = data['createdDate']
        self.updatedDate = data['updatedDate']
        self.userId = data['userId']
        self.likes = []
        self.listingOwner = {
            'firstName' : '',
            'lastName' : ''
        }

# Confirm fields are filled out
    @staticmethod
    def validate_listing(listing):
        is_valid = True
        if len(listing['title']) < 1:
            flash("Please provide a title for this listing.")
            is_valid = False
        if len(listing['description']) < 20:
            flash("Please provide a description longer than 20 characters.")
            is_valid = False
        if len(listing['listPrice']) < 0.01:
            flash("Please provide a price for this listing.")
            is_valid = False
        return is_valid

# Confirm edit fields are still filled out
    @staticmethod
    def validate_edit(listing):
        is_valid = True
        if len(listing['title']) < 1:
            flash("Please provide a title for this listing.")
            is_valid = False
        if len(listing['description']) < 20:
            flash("PLease provide a description longer than 20 characters.")
            is_valid = False
        if len(listing['listPrice']) < 0.01:
            flash("Please provide a price for this listing.")
            is_valid = False
        return is_valid

# Save new home listing
    @classmethod
    def save_listing(cls, data):
        query = "INSERT INTO listings (title, description, listPrice, imgURL, createdDate, updatedDate, userId) VALUES (%(title)s, %(description)s, %(listPrice)s, %(imgURL)s, NOW(), NOW(), %(userId)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

# Get all home listings, for public listing page
    @classmethod
    def get_listings(cls):
        query = "SELECT * FROM listings LEFT JOIN users ON listings.userId = users.id WHERE userId = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        if not results:
            return False
        
        all_listings = []

        for row in results:
            row['likes'] = Listings.get_listing_likes(row)
            all_listings.append(row)
        
        return all_listings

# Get all home listings, for public listing page
    @classmethod
    def get_one_listing(cls, data):
        query = "SELECT * FROM listings LEFT JOIN users ON listings.userId = users.id WHERE listings.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if not results:
            return False

        current_listing = cls(results[0])

        current_listing.listingOwner['firstName'] = results[0]['firstName']
        current_listing.listingOwner['lastName'] = results[0]['lastName']

        return current_listing

# Edit home listing
    @classmethod
    def update_listing(cls, data):
        query = "UPDATE listings SET title=%(title)s, description=%(description)s, listPrice=%(listPrice)s, imgURL=%(imgURL)s, updatedDate=NOW() WHERE id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

# Delete home listing
    @classmethod
    def delete_listing(cls, data):
        #delete likes
        query = "DELETE FROM likes WHERE listingID = %(id)s;"

        connectToMySQL(cls.db_name).query_db(query, data)

        #delete listing
        query = "DELETE FROM listings WHERE id = %(id)s;"
        
        return connectToMySQL(cls.db_name).query_db(query, data)


# Like a listing
    @classmethod
    def like_listing(cls, data):
        query = "INSERT INTO likes (userID, listingID) VALUES (%(userID)s, %(listingID)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    # Unlike a listing
    @classmethod
    def unlike_listing(cls, data):
        query = "DELETE FROM likes WHERE userID = %(userID)s and listingID = %(listingID)s;"
        
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_listing_likes(cls, data):

        query = "SELECT DISTINCT userID FROM likes WHERE listingID = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)

        if not result:
            return result

        liked_users = []

        for row in result: 
            liked_users.append(row)

        return liked_users

    @classmethod
    def get_favorite_listings(cls, data):

        query = "SELECT l.*,firstName,lastName FROM listings l JOIN users U on u.id = l.userId join likes li on li.listingID = l.id and li.userID = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)

        if not result:
            return result

        favorite_listings = []

        for row in result: 
            favorite_listings.append(row)

        return favorite_listings
