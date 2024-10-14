import sys
import os
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(base_dir)

import unittest
from unittest.mock import MagicMock
from dao.VirtualArtGalleryImpl import VirtualArtGalleryImpl
from entity.artwork import Artwork

class TestArtworkManagement(unittest.TestCase):
    def setUp(self):
        self.service = VirtualArtGalleryImpl()

    def test_add_artwork_success(self):
        self.service.connection = MagicMock()
        cursor_mock = self.service.connection.cursor.return_value
        cursor_mock.execute.return_value = None
        artwork = Artwork(artworkId="101",
                            title="Testing", 
                            description="Test Description", 
                            creationDate="2024-03-31", 
                            medium="english", 
                            imageURL="http://test.jpg")
        result = self.service.addArtwork(artwork)
        self.assertTrue(result)
        cursor_mock.execute.assert_called_once()

    def test_add_artwork_failure(self):
        self.service.connection = MagicMock()
        cursor_mock = self.service.connection.cursor.return_value
        cursor_mock.execute.side_effect = Exception("Mocked DB Error")
        artwork = Artwork(artworkId="101", 
                            title="Testing", 
                            description="Test Description", 
                            creationDate="2024-03-31",
                            medium="english", 
                            imageURL="http://test.jpg")
        result = self.service.addArtwork(artwork)
        self.assertFalse(result)
        cursor_mock.execute.assert_called_once()

    def test_update_artwork_success(self):
        self.service.connection = MagicMock()
        mock_cursor = MagicMock()
        self.service.connection.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        updated_artwork = Artwork(artworkId="1",
                                    title="Updated Title",
                                    description="Updated Description",
                                    creationDate="2024-05-13",
                                    medium="french", 
                                    imageURL="http://updated_artwork.jpg")
        result = self.service.updateArtwork(updated_artwork,updated_artwork.artworkId)
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()

    def test_update_artwork_failure(self):
        self.service.connection = MagicMock()
        cursor_mock = self.service.connection.cursor.return_value
        cursor_mock.execute.side_effect = Exception("Mocked DB Error")
        updated_artwork = Artwork(artworkId="1",
                                    title="Updated Title", 
                                    description="Updated Description",
                                    creationDate="2024-05-13", 
                                    medium="french", 
                                    imageURL="http://updated_artwork.jpg")
        result = self.service.updateArtwork(updated_artwork,updated_artwork.artworkId)
        self.assertFalse(result)
        cursor_mock.execute.assert_called_once()

    
    def test_remove_artwork_success(self):
        self.service.connection = MagicMock()
        cursor_mock = self.service.connection.cursor.return_value
        cursor_mock.execute.return_value = None
        artwork_id = "1"
    
        result = self.service.removeArtwork(artwork_id)
        self.assertTrue(result)

        # Assert that execute was called 4 times
        self.assertEqual(cursor_mock.execute.call_count, 4)

        # Verify the calls were made with the correct arguments
        cursor_mock.execute.assert_any_call("SELECT Count(*) FROM Artwork WHERE ArtworkID=?", (artwork_id,))
        cursor_mock.execute.assert_any_call("DELETE FROM User_Favorite_Artwork WHERE ArtworkID=?", (artwork_id,))
        cursor_mock.execute.assert_any_call("DELETE FROM Artwork_Gallery WHERE ArtworkID=?", (artwork_id,))
        cursor_mock.execute.assert_any_call("DELETE FROM Artwork WHERE ArtworkID=?", (artwork_id,))


    def test_remove_artwork_failure(self):
        self.service.connection = MagicMock()
        cursor_mock = self.service.connection.cursor.return_value
        cursor_mock.execute.side_effect = Exception("Mocked DB Error")
        artwork_id = "1"
        result = self.service.removeArtwork(artwork_id)
        self.assertFalse(result)
        cursor_mock.execute.assert_called_once()

    def test_search_artworks_success(self):
        self.service.connection = MagicMock()
        mock_cursor = MagicMock()
        self.service.connection.cursor.return_value = mock_cursor

        # Mock the fetchall return value to match the database schema
        mock_cursor.fetchall.return_value = [
        (1, 'Artwork 1', 'Description 1', '2024-05-15', 'Medium 1', 'image1.jpg'),
        (2, 'Artwork 2', 'Description 2', '2024-05-16', 'Medium 2', 'image2.jpg')
        ]

        search_term = "elephant"
        artworks = self.service.searchArtworks(search_term)
    
        # Debug print to check the result of searchArtworks
        #print("Artworks returned from search:", artworks)

        self.assertIsInstance(artworks, list)
        self.assertEqual(len(artworks), 2)
        self.assertEqual(artworks[0].get_title(), 'Artwork 1')
        self.assertEqual(artworks[1].get_title(), 'Artwork 2')
        


if __name__ == '__main__':
    unittest.main()
