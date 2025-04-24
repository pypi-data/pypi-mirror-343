import unittest

import numpy as np

import fcl


# These test cases were added because there was a very sneaky crash that would occur
# in the signed distance functions if all libs were not compiled with double precision
class TestPrecision(unittest.TestCase):
    def setUp(self):
        self.act_dist = -0.00735518

        # Set up first mesh
        f1 = np.array(
            [
                [0, 1, 2],
                [0, 2, 3],
                [3, 4, 5],
                [3, 5, 0],
                [2, 6, 4],
                [2, 4, 3],
                [1, 7, 6],
                [1, 6, 2],
                [7, 5, 4],
                [7, 4, 6],
                [0, 5, 7],
                [0, 7, 1],
            ]
        )
        tris1 = np.concatenate(
            (3 * np.ones((len(f1), 1), dtype=np.int64), f1), axis=1
        ).flatten()
        v1 = np.array(
            [
                [-1.5596524477005005, -1.4861732721328735, 0.0],
                [-1.55965256690979, -1.3408161401748657, 0.0],
                [0.8114118576049805, -1.3408160209655762, 0.0],
                [0.8114122152328491, -1.4861732721328735, 0.0],
                [0.8114122152328491, -1.4861732721328735, 2.566922187805176],
                [-1.559652328491211, -1.4861699342727661, 2.566922187805176],
                [0.8114122152328491, -1.3408160209655762, 2.566922187805176],
                [-1.5596498250961304, -1.3408160209655762, 2.566922187805176],
            ]
        )
        t1 = np.zeros(3)
        r1 = np.eye(3)

        # Set up second mesh
        f2 = np.array(
            [
                [0, 1, 2],
                [0, 2, 3],
                [3, 2, 4],
                [3, 4, 5],
                [5, 4, 6],
                [5, 6, 7],
                [7, 6, 1],
                [7, 1, 0],
                [3, 5, 7],
                [3, 7, 0],
                [4, 2, 1],
                [4, 1, 6],
            ]
        )
        tris2 = np.concatenate(
            (3 * np.ones((len(f2), 1), dtype=np.int64), f2), axis=1
        ).flatten()
        v2 = np.array(
            [
                [-0.035486817359924316, -0.15411892533302307, 0.08323988318443298],
                [-0.035486817359924316, -0.034327179193496704, 0.13931824266910553],
                [-0.035486817359924316, -0.004236131906509399, 0.07503926753997803],
                [-0.035486817359924316, -0.12402787804603577, 0.018960915505886078],
                [0.035486817359924316, -0.004236131906509399, 0.07503926753997803],
                [0.035486817359924316, -0.12402787804603577, 0.018960915505886078],
                [0.035486817359924316, -0.034327179193496704, 0.13931824266910553],
                [0.035486817359924316, -0.15411892533302307, 0.08323988318443298],
            ]
        )
        t2 = np.array([-0.17816561357553456, -1.1899346069644454, 1.1061233975645952])
        r2 = np.array(
            [
                [-0.7731251991739131, 0.3586043541062879, -0.5231446679631834],
                [0.4540350514442685, 0.8888443213778688, -0.06170854409493361],
                [0.4428652147801832, -0.28523444667558645, -0.8500068893646534],
            ]
        )

        # Wrap meshes in FCL Convex objects
        c1 = fcl.Convex(v1, len(f1), tris1)
        c2 = fcl.Convex(v2, len(f2), tris2)

        # Wrap in CollisionObjects
        self.o1 = fcl.CollisionObject(c1, fcl.Transform(r1, t1))
        self.o2 = fcl.CollisionObject(c2, fcl.Transform(r2, t2))

        # Create managers
        self.mgr1 = fcl.DynamicAABBTreeCollisionManager()
        self.mgr2 = fcl.DynamicAABBTreeCollisionManager()

        self.mgr1.registerObjects([self.o1])
        self.mgr2.registerObjects([self.o2])

        self.mgr1.setup()
        self.mgr2.setup()

    def test_obj_obj_coll(self):
        request = fcl.CollisionRequest()
        result = fcl.CollisionResult()
        ret = fcl.collide(self.o1, self.o2, request, result)
        assert ret == 1  # Objects are in collision

        request = fcl.CollisionRequest()
        result = fcl.CollisionResult()
        ret = fcl.collide(self.o2, self.o1, request, result)
        assert ret == 1  # Objects are in collision

    def test_obj_obj_simple_distance(self):
        request = fcl.DistanceRequest()
        result = fcl.DistanceResult()
        ret = fcl.distance(self.o1, self.o2, request, result)
        assert ret == -1

        request = fcl.DistanceRequest()
        result = fcl.DistanceResult()
        ret = fcl.distance(self.o2, self.o1, request, result)
        assert ret == -1

    def test_obj_obj_signed_distance(self):
        request = fcl.DistanceRequest(
            enable_nearest_points=True, enable_signed_distance=True
        )
        result = fcl.DistanceResult()
        ret = fcl.distance(self.o1, self.o2, request, result)
        assert np.isclose(ret, self.act_dist)
        assert np.isclose(np.linalg.norm(np.subtract(*result.nearest_points)), abs(ret))

        request = fcl.DistanceRequest(
            enable_nearest_points=True, enable_signed_distance=True
        )
        result = fcl.DistanceResult()
        ret = fcl.distance(self.o2, self.o1, request, result)
        assert np.isclose(ret, self.act_dist)
        assert np.isclose(np.linalg.norm(np.subtract(*result.nearest_points)), abs(ret))

    def test_mgr_obj_coll(self):
        req = fcl.CollisionRequest(num_max_contacts=100, enable_contact=True)
        rdata = fcl.CollisionData(request=req)
        self.mgr1.collide(self.o2, rdata, fcl.defaultCollisionCallback)
        assert rdata.result.is_collision

        rdata = fcl.CollisionData(request=req)
        self.mgr2.collide(self.o1, rdata, fcl.defaultCollisionCallback)
        assert rdata.result.is_collision

    def test_mgr_mgr_coll(self):
        req = fcl.CollisionRequest(num_max_contacts=100, enable_contact=True)
        rdata = fcl.CollisionData(request=req)
        self.mgr1.collide(self.mgr2, rdata, fcl.defaultCollisionCallback)
        assert rdata.result.is_collision

        rdata = fcl.CollisionData(request=req)
        self.mgr2.collide(self.mgr1, rdata, fcl.defaultCollisionCallback)
        assert rdata.result.is_collision

    def test_mgr_obj_signed_distance(self):
        req = fcl.DistanceRequest(enable_signed_distance=True, enable_nearest_points=True)
        ddata = fcl.DistanceData(req)
        self.mgr1.distance(self.o2, ddata, fcl.defaultDistanceCallback)
        assert np.isclose(ddata.result.min_distance, self.act_dist)
        assert np.isclose(
            np.linalg.norm(np.subtract(*ddata.result.nearest_points)),
            abs(ddata.result.min_distance),
        )

        req = fcl.DistanceRequest(enable_signed_distance=True, enable_nearest_points=True)
        ddata = fcl.DistanceData(req)
        self.mgr2.distance(self.o1, ddata, fcl.defaultDistanceCallback)
        assert np.isclose(ddata.result.min_distance, self.act_dist)
        assert np.isclose(
            np.linalg.norm(np.subtract(*ddata.result.nearest_points)),
            abs(ddata.result.min_distance),
        )

    def test_mgr_mgr_signed_distance(self):
        req = fcl.DistanceRequest(enable_signed_distance=True, enable_nearest_points=True)
        ddata = fcl.DistanceData(req)
        self.mgr1.distance(self.mgr2, ddata, fcl.defaultDistanceCallback)
        assert np.isclose(ddata.result.min_distance, self.act_dist)
        assert np.isclose(
            np.linalg.norm(np.subtract(*ddata.result.nearest_points)),
            abs(ddata.result.min_distance),
        )

        req = fcl.DistanceRequest(enable_signed_distance=True, enable_nearest_points=True)
        ddata = fcl.DistanceData(req)
        self.mgr2.distance(self.mgr1, ddata, fcl.defaultDistanceCallback)
        assert np.isclose(ddata.result.min_distance, self.act_dist)
        assert np.isclose(
            np.linalg.norm(np.subtract(*ddata.result.nearest_points)),
            abs(ddata.result.min_distance),
        )
