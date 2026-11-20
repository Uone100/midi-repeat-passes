import unittest
from examples.make_demo import make
from scripts.passes import apply
class Passes(unittest.TestCase):
    def test_even_passes_and_duration(self):
        f=make(); leader=f.tracks[0].copy()
        result=apply(f,1,0,480,4,{2,4})
        self.assertEqual(result["removed_onsets_by_pass"],[1,0,1,0])
        self.assertEqual(f.tracks[0],leader)
        self.assertEqual(sum(x.time for x in f.tracks[1]),1920)
        self.assertEqual([x.note for x in f.tracks[1] if x.type=="note_on"],[49,51])
    def test_short_file(self):
        with self.assertRaises(ValueError): apply(make(),1,0,960,4,{2})
