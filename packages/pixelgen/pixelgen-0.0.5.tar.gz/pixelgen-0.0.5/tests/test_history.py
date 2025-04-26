import unittest
import numpy as np
from pixelgen.core import PixelGenerator

class TestHistoryManagement(unittest.TestCase):
    def setUp(self):
        self.pixel_gen = PixelGenerator(32, 32)

    def test_initial_state(self):
        """Test that initial state is properly saved"""
        initial_state = np.zeros((32, 32, 3), dtype=np.uint8)
        self.assertTrue(np.array_equal(self.pixel_gen.canvas, initial_state))
        self.assertEqual(len(self.pixel_gen.history), 1)
        self.assertEqual(len(self.pixel_gen.redo_stack), 0)

    def test_undo_redo(self):
        """Test basic undo/redo functionality"""
        # Initial state should be all zeros
        initial_state = np.zeros((32, 32, 3), dtype=np.uint8)
        self.assertTrue(np.array_equal(self.pixel_gen.canvas, initial_state))
        
        # Make a change
        self.pixel_gen.fill_area(0, 0, 10, 10, (255, 0, 0))
        red_state = self.pixel_gen.canvas.copy()
        
        # Verify red area was created
        self.assertTrue(np.all(self.pixel_gen.canvas[0:10, 0:10] == [255, 0, 0]))
        
        # Undo should restore to initial state
        self.pixel_gen.undo()
        self.assertTrue(np.array_equal(self.pixel_gen.canvas, initial_state))
        
        # Redo should restore the red area
        self.pixel_gen.redo()
        self.assertTrue(np.array_equal(self.pixel_gen.canvas, red_state))

    def test_multiple_undo_redo(self):
        """Test multiple undo/redo operations"""
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        states = [self.pixel_gen.canvas.copy()]  # Initial state
        
        # Apply colors and save states
        for color in colors:
            self.pixel_gen.fill_area(0, 0, 10, 10, color)
            states.append(self.pixel_gen.canvas.copy())
        
        # Verify all states were created
        self.assertEqual(len(states), len(colors) + 1)
        
        # Undo all changes
        for i in range(len(colors)):
            self.pixel_gen.undo()
            self.assertTrue(np.array_equal(self.pixel_gen.canvas, states[len(colors)-i-1]))
        
        # Redo all changes
        for i in range(len(colors)):
            self.pixel_gen.redo()
            self.assertTrue(np.array_equal(self.pixel_gen.canvas, states[i+1]))

    def test_undo_limit(self):
        """Test that undo stops at initial state"""
        initial_state = self.pixel_gen.canvas.copy()
        
        # Try to undo when no changes made
        result = self.pixel_gen.undo()
        self.assertFalse(result)
        self.assertTrue(np.array_equal(self.pixel_gen.canvas, initial_state))

    def test_redo_limit(self):
        """Test that redo stops at most recent state"""
        # Make a change
        self.pixel_gen.fill_area(0, 0, 10, 10, (255, 0, 0))
        final_state = self.pixel_gen.canvas.copy()
        
        # Undo and redo
        self.pixel_gen.undo()
        self.pixel_gen.redo()
        
        # Try to redo again
        result = self.pixel_gen.redo()
        self.assertFalse(result)
        self.assertTrue(np.array_equal(self.pixel_gen.canvas, final_state))

    def test_new_action_clears_redo(self):
        """Test that new actions clear the redo stack"""
        # Make initial changes
        self.pixel_gen.fill_area(0, 0, 10, 10, (255, 0, 0))
        self.pixel_gen.fill_area(0, 0, 10, 10, (0, 255, 0))
        
        # Undo once
        self.pixel_gen.undo()
        
        # Make new change
        self.pixel_gen.fill_area(0, 0, 10, 10, (0, 0, 255))
        
        # Try to redo - should fail
        result = self.pixel_gen.redo()
        self.assertFalse(result)