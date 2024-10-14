from typing import List

from dao.IvirtualArtGallery import IVirtualArtGallery
from entity.artwork import Artwork
from entity.gallery import Gallery
from exception.ArtWorkNotFoundException import ArtWorkNotFoundException
from exception.UserNotFoundException import UserNotFoundException
from util.DBConnection import DBConnection
from tabulate import tabulate


class VirtualArtGalleryImpl(IVirtualArtGallery):
    connection=None
    def __init__(self):
        self.connection=DBConnection.getConnection()

    def get_next_artworkID(self):
        conn = DBConnection.getConnection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Max(ArtworkID) FROM Artwork")
            max_id = cursor.fetchone()[0]
            return (max_id + 1) if max_id is not None else 1
        except Exception as e:
            print(e)
            return 1
        finally:
            cursor.close()

    def addArtwork(self, artwork):
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO Artwork (ArtworkID,Title,Description,CreationDate,Medium,ImageURL) VALUES (?,?,?,?,?,?)"
            cursor.execute(query,(self.get_next_artworkID(),artwork.get_title(),artwork.get_description(),artwork.get_creationDate(),artwork.get_medium(),artwork.get_imageURL()))
            self.connection.commit()
            print("------Artwork added------")
            return True
        except Exception as e:
            print("------Error in adding Artwork------",e)
            self.connection.rollback()
            return False
        finally:
            cursor.close()


    def updateArtwork(self, artwork, artworkId):
        cursor = self.connection.cursor()
        try:
        
            query = "UPDATE Artwork SET "
            params = []
        
            if artwork.get_title():
                query += "Title=?, "
                params.append(artwork.get_title())
            if artwork.get_description():
                query += "Description=?, "
                params.append(artwork.get_description())
            if artwork.get_creationDate():
                query += "CreationDate=?, "
                params.append(artwork.get_creationDate())
            if artwork.get_medium():
                query += "Medium=?, "
                params.append(artwork.get_medium())
            if artwork.get_imageURL():
                query += "ImageURL=?, "
                params.append(artwork.get_imageURL())
        
      
            query = query.rstrip(", ")
            query += " WHERE ArtworkID=?"
            params.append(artworkId)
        
            cursor.execute(query, tuple(params))
            self.connection.commit()
            print("------Artwork updated------")
            return True

        except Exception as e:
            print("------Error in updating Artwork------", e)
            return False
        finally:
            cursor.close()

    def removeArtwork(self, artworkId):
        cursor = self.connection.cursor()
        try:
            query = "SELECT Count(*) FROM Artwork WHERE ArtworkID=?"
            cursor.execute(query,(artworkId,))
            count = cursor.fetchone()[0]
            if count == 0:
                raise ArtWorkNotFoundException(artworkId)
            
            # Remove any references in User_Favorite_Artwork table
            delete_favorites_query = "DELETE FROM User_Favorite_Artwork WHERE ArtworkID=?"
            cursor.execute(delete_favorites_query, (artworkId,))

            # Remove any references in Artwork_Gallery table
            delete_gallery_query = "DELETE FROM Artwork_Gallery WHERE ArtworkID=?"
            cursor.execute(delete_gallery_query, (artworkId,))

       
            query='DELETE FROM Artwork WHERE ArtworkID=?'
            cursor.execute(query,(artworkId,))
            self.connection.commit()
            print("------Artwork removed------")
            return True
        
        
        except ArtWorkNotFoundException as e:
            print(e)  
            return False 
     
        except Exception as e:
            print("------Error in removing Artwork------",e)
            self.connection.rollback()
            return False
        finally:
            cursor.close()


    def updateGallery(self, gallery):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Gallery SET name = %s, description = %s, location = %s, curator = %s, openinghours = %s WHERE GalleryID = %s"
            cursor.execute(query, (
                gallery.get_name(), gallery.get_description(), gallery.get_location(), gallery.get_curator(),
                gallery.get_opening_hours(), gallery.get_gallery_id()))
            self.connection.commit()
            print("Gallery updated")
            return True
        except Exception as e:
            print("Error updating gallery", e)
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def getArtworkById(self, artworkId: int) -> Artwork:
        try:
            cursor = self.connection.cursor()
            query = 'SELECT * FROM Artwork WHERE ArtworkID=?'
            cursor.execute(query, (artworkId,))
            artwork = cursor.fetchone()
            if artwork is None: 
                raise ArtWorkNotFoundException(artworkId)
            else:
                artwork_details = [
                    ['ArtworkID', artwork[0]],
                    ['Title', artwork[1]],
                    ['Description', artwork[2]],
                    ['CreationDate', artwork[3]],
                    ['Medium', artwork[4]],
                    ['ImageURL', artwork[5]],
                ]
                print("Artwork details")
                print(tabulate(artwork_details, tablefmt="grid"))
                return artwork
        except ArtWorkNotFoundException as e:
            print(e)
        except Exception as e:
            print("Error in getting the details:",e)
        finally:
            cursor.close()


    def searchArtworks(self, search_object) -> list[Artwork]:
        cursor = self.connection.cursor()
        artworks = []
        try:
            query = 'SELECT * FROM Artwork WHERE Title LIKE ? OR Medium LIKE ? OR Description LIKE ?'
            cursor.execute(query, (f'%{search_object}%', f'%{search_object}%', f'%{search_object}%'))
            artwork_data = cursor.fetchall()

            if artwork_data:
                artwork_table = [] 
                for artwork in artwork_data:
                    artwork_details = Artwork(
                        artworkId=artwork[0],     # Assuming ArtworkID is the first column
                        title=artwork[1],         # Title is the second column
                        description=artwork[2],   # Description is the third column
                        creationDate=artwork[3],  # CreationDate is the fourth column
                        medium=artwork[4],        # Medium is the fifth column
                        imageURL=artwork[5]       # ImageURL is the sixth column
                    )
                    artworks.append(artwork_details)
                    # Prepare a list of artwork details for printing
                    artwork_table.append([
                        artwork_details.artworkId,
                        artwork_details.title,
                        artwork_details.description,
                        artwork_details.creationDate,
                        artwork_details.medium,
                        artwork_details.imageURL
                    ])
            
                # Print the artwork details using tabulate
                print("Artworks found:")
                print(tabulate(artwork_table, headers=["Artwork ID", "Title",
                                                    "Description", "Creation Date", 
                                                    "Medium", "Image URL"], tablefmt="grid"))
                    
                   
                    
                return artworks
            else:
                print("No artwork found matching the search term")
                return artworks 
        except Exception as e:
            print("Error in searching artworks:",e)
            self.connection.rollback()
            return []
        finally:
            cursor.close()

    def addArtworkToFavorite(self, userId, artworkId) -> bool:
        cursor = self.connection.cursor()
        try:
            
            query = "SELECT * FROM Artwork WHERE ArtworkID=?"
            cursor.execute(query, (artworkId,))
            if cursor.fetchone() is None:
                raise ArtWorkNotFoundException(artworkId)

            query = 'INSERT INTO User_Favorite_Artwork(UserID,ArtworkID) VALUES (?,?)'
            cursor.execute(query, (userId, artworkId))
            self.connection.commit()
            print("Added to favorites")
            return True
        
        
        except ArtWorkNotFoundException as e:
            print(e)
            return False
        
        finally:
            cursor.close()

    def removeArtworkFromFavorite(self, userId, artworkId) -> bool:
        cursor = self.connection.cursor()
        try:
            
            query = "SELECT * FROM Artwork WHERE ArtworkID=?"
            cursor.execute(query, (artworkId,))
            if cursor.fetchone() is None:
                raise ArtWorkNotFoundException(artworkId)

            query = "DELETE FROM User_Favorite_Artwork WHERE UserID=? AND ArtworkID=?"
            cursor.execute(query, (userId, artworkId))
            self.connection.commit()
            print("Removed from favorites")
            return True
        
       
        except ArtWorkNotFoundException as e:
            print(e)
            return False

        finally:
            cursor.close()

    def getUserFavoriteArtworks(self, userId):
        cursor = self.connection.cursor()
        try:
            query = 'SELECT a.* FROM Artwork a JOIN User_Favorite_Artwork u on a.ArtworkID=u.ArtworkID WHERE UserID=?'
            cursor.execute(query, (userId,))
            artwork_data = cursor.fetchall()
            if artwork_data:
                for artwork in artwork_data:
                    artwork_details = [
                        ['Artwork ID', artwork[0]],
                        ['Title', artwork[1]],
                        ['Description', artwork[2]],
                        ['CreationDate', artwork[3]],
                        ['Medium', artwork[4]],
                        ['ImageURL', artwork[5]]
                    ]
                    print(tabulate(artwork_details, tablefmt="grid"))
            else:
                raise UserNotFoundException(userId)
        except Exception as e:
            print(e)
        finally:
            cursor.close()


    def add_gallery(self, gallery):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Gallery (name, description, location, curator, openinghours) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (
            gallery.get_name(), gallery.get_description(), gallery.get_location(), gallery.get_curator(),
            gallery.get_openingHours()))
            self.connection.commit()
            print("Gallery added")
            return True
        except Exception as e:
            print("Error adding gallery", e)
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def update_gallery(self, gallery):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Gallery SET name = %s, description = %s, location = %s, curator = %s, openinghours = %s WHERE GalleryID = %s"
            cursor.execute(query, (
                gallery.get_name(), gallery.get_description(), gallery.get_location(), gallery.get_curator(),
                gallery.get_openingHours(), gallery.get_galleryId()))
            self.connection.commit()
            print("Gallery updated")
            return True
        except Exception as e:
            print("Error updating gallery", e)
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def delete_gallery(self, galleryId):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Gallery WHERE GalleryID = %s"
            cursor.execute(query, (galleryId,))
            self.connection.commit()
            print("Gallery deleted")
            return True
        except Exception as e:
            print("Error deleting gallery", e)
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def search_galleries(self, search_term: str) ->list[Gallery]:
        cursor=None
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Gallery WHERE Name LIKE %s OR Description LIKE %s"
            cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
            galleries_data = cursor.fetchall()
            galleries = []
            for gallery_data in galleries_data:
                gallery = Gallery(
                    gallery_data['GalleryID'],
                    gallery_data['Name'],
                    gallery_data['Description'],
                    gallery_data['Location'],
                    gallery_data['Curator'],
                    gallery_data['OpeningHours']
                )
                galleries.append(gallery)
            return galleries
        except Exception as e:
            print("Error searching galleries:", e)
            return []
        finally:
            cursor.close()









