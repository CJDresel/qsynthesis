import logging
from pathlib import Path

from qtracedb import DatabaseManager

from qsynthesis.utils.qtrace_symexec import QtraceSymExec, Mode
from qsynthesis.algorithms import TopDownSynthesizer
from qsynthesis.tables import LookupTableLevelDB

logging.basicConfig(level=logging.DEBUG)

CURRENT_DIR = Path(__file__).parent.absolute()
DATABASE_FILE = CURRENT_DIR / "../../qsynth-dataset-and-artifact/datasets/custom_EA/trace.db"
TABLE_DIR = CURRENT_DIR / "../lts/lts15_opt_leveldb"

TARGETS =  [(99, 157), (164, 238), (245, 257), (264, 303), (310, 424), (431, 622), (629, 671), (678, 783), (790, 876),
            (883, 937), (944, 1033), (1040, 1052), (1059, 1078), (1085, 1106), (1113, 1140), (1147, 1221), (1228, 1356),
            (1363, 1432), (1439, 1629), (1636, 1695), (1702, 1719), (1726, 1753), (1760, 1791), (1798, 1818), (1825, 1864),
            (1871, 1884), (1891, 2159), (2166, 2178), (2185, 2573), (2580, 2591), (2598, 2769), (2776, 2796), (2803, 2999),
            (3006, 3067), (3074, 3120), (3127, 3156), (3163, 3186), (3193, 3260), (3267, 3327), (3334, 3358), (3365, 3570),
            (3577, 3597), (3604, 3650), (3657, 3717), (3724, 3774), (3781, 3852), (3859, 3872), (3879, 3962), (3969, 3984),
            (3991, 4207), (4214, 4252), (4259, 4400), (4407, 4427), (4434, 4453), (4460, 4598), (4605, 4705), (4712, 4772),
            (4779, 4968), (4975, 5075), (5082, 5114), (5121, 5165), (5172, 5201), (5208, 5233), (5240, 5276), (5283, 5308),
            (5315, 5349), (5356, 5393), (5400, 5449), (5456, 5640), (5647, 5666), (5673, 5806), (5813, 6310), (6317, 6345),
            (6352, 6402), (6409, 6448), (6455, 6482), (6489, 6506), (6513, 6581), (6588, 6619), (6626, 6677), (6684, 6746),
            (6753, 6764), (6771, 6914), (6921, 6963), (6970, 7033), (7040, 7057), (7064, 7137), (7144, 7182), (7189, 7264),
            (7271, 7309), (7316, 7346), (7353, 7543), (7550, 7561), (7568, 7587), (7594, 7705), (7712, 7723), (7730, 7775),
            (7782, 7914), (7921, 7958), (7965, 8028), (8035, 8130), (8137, 8172), (8179, 8226), (8233, 8298), (8305, 8316),
            (8323, 8350), (8357, 8775), (8782, 8850), (8857, 8883), (8890, 8980), (8987, 9054), (9061, 9138), (9145, 9212),
            (9219, 9278), (9285, 9298), (9305, 9475), (9482, 9607), (9614, 9656), (9663, 9697), (9704, 9720), (9727, 9830),
            (9837, 10068), (10075, 10348), (10355, 10370), (10377, 10567), (10574, 10604), (10611, 10662), (10669, 10822),
            (10829, 10952), (10959, 10970), (10977, 10988), (10995, 11031), (11038, 11122), (11129, 11166), (11173, 11406),
            (11413, 11508), (11515, 11729), (11736, 11768), (11775, 11805), (11812, 11825), (11832, 12006), (12013, 12032),
            (12039, 12636), (12643, 12748), (12755, 12836), (12843, 12966), (12973, 13012), (13019, 13217), (13224, 13258),
            (13265, 13436), (13443, 13575), (13582, 13918), (13925, 13964), (13971, 14021), (14028, 14101), (14108, 14129),
            (14136, 14211), (14218, 14229), (14236, 14466), (14473, 14500), (14507, 14532), (14539, 14551), (14558, 14614),
            (14621, 14656), (14663, 14735), (14742, 14753), (14760, 14840), (14847, 14878), (14885, 14961), (14968, 15142),
            (15149, 15389), (15396, 15503), (15510, 15864), (15871, 16028), (16035, 16114), (16121, 16149), (16156, 16306),
            (16313, 16390), (16397, 16473), (16480, 16500), (16507, 16524), (16531, 16698), (16705, 16786), (16793, 16811),
            (16818, 16854), (16861, 16927), (16934, 16945), (16952, 16997), (17004, 17065), (17072, 17095), (17102, 17133),
            (17140, 17286), (17293, 17496), (17503, 17518), (17525, 17582), (17589, 17622), (17629, 17792), (17799, 17847),
            (17854, 17924), (17931, 17999), (18006, 18032), (18039, 18238), (18245, 18295), (18302, 18591), (18598, 18892),
            (18899, 19118), (19125, 19270), (19277, 19336), (19343, 19373), (19380, 19631), (19638, 19764), (19771, 19873),
            (19880, 19897), (19904, 20160), (20167, 20180), (20187, 20245), (20252, 20465), (20472, 21063), (21070, 21091),
            (21098, 21130), (21137, 21216), (21223, 21251), (21258, 21330), (21337, 21507), (21514, 21789), (21796, 21928),
            (21935, 21967), (21974, 22058), (22065, 22146), (22153, 22230), (22237, 22382), (22389, 22458), (22465, 22484),
            (22491, 22514), (22521, 22578), (22585, 22604), (22611, 22649), (22656, 22739), (22746, 22790), (22797, 22808),
            (22815, 22853), (22860, 22895), (22902, 23058), (23065, 23076), (23083, 23357), (23364, 23430), (23437, 23519),
            (23526, 23634), (23641, 23652), (23659, 23686), (23693, 23797), (23804, 23932), (23939, 24024), (24031, 24098),
            (24105, 24226), (24233, 24303), (24310, 24379), (24386, 24469), (24476, 24573), (24580, 24955), (24962, 24995),
            (25002, 25056), (25063, 25137), (25144, 25741), (25748, 25856), (25863, 25962), (25969, 26013), (26020, 26033),
            (26040, 26201), (26208, 26222), (26229, 26317), (26324, 26465), (26472, 26504), (26511, 26532), (26539, 26760),
            (26767, 26812), (26819, 26941), (26948, 27061), (27068, 27119), (27126, 27241), (27248, 27329), (27336, 27563),
            (27570, 27600), (27607, 27667), (27674, 27885), (27892, 27947), (27954, 27975), (27982, 28077), (28084, 28210),
            (28217, 28241), (28248, 28348), (28355, 28372), (28379, 28398), (28405, 28617), (28624, 28682), (28689, 28749),
            (28756, 28774), (28781, 28792), (28799, 28814), (28821, 28907), (28914, 28965), (28972, 28991), (28998, 29032),
            (29039, 29767), (29774, 29809), (29816, 29842), (29849, 29879), (29886, 29983), (29990, 30031), (30038, 30072),
            (30079, 30151), (30158, 30174), (30181, 30546), (30553, 30574), (30581, 30659), (30666, 30684), (30691, 31057),
            (31064, 31118), (31125, 31166), (31173, 31200), (31207, 31253), (31260, 31282), (31289, 31507), (31514, 31631),
            (31638, 31675), (31682, 31726), (31733, 31870), (31877, 31920), (31927, 31956), (31963, 32018), (32025, 32066),
            (32073, 32127), (32134, 32241), (32248, 32389), (32396, 32430), (32437, 32482), (32489, 32510), (32517, 32538),
            (32545, 32650), (32657, 33029), (33036, 33126), (33133, 33158), (33165, 33290), (33297, 33443), (33450, 33479),
            (33486, 33506), (33513, 33544), (33551, 33656), (33663, 33778), (33785, 33939), (33946, 34031), (34038, 34067),
            (34074, 34217), (34224, 34253), (34260, 34352), (34359, 34670), (34677, 35060), (35067, 35256), (35263, 35287),
            (35294, 35365), (35372, 35470), (35477, 35504), (35511, 35562), (35569, 35580), (35587, 35679), (35686, 35856),
            (35863, 35881), (35888, 35911), (35918, 36075), (36082, 36101), (36108, 36143), (36150, 36214), (36221, 36288),
            (36295, 36638), (36645, 36657), (36664, 36684), (36691, 36831), (36838, 36940), (36947, 36976), (36983, 37043),
            (37050, 37181), (37188, 37201), (37208, 37237), (37244, 37270), (37277, 37336), (37343, 37527), (37534, 37708),
            (37715, 37895), (37902, 37956), (37963, 37991), (37998, 38014), (38021, 38046), (38053, 38344), (38351, 38405),
            (38412, 38557), (38564, 38650), (38657, 38719), (38726, 38862), (38869, 38915), (38922, 39204), (39211, 39266),
            (39273, 39313), (39320, 39701), (39708, 40103), (40110, 40129), (40136, 40188), (40195, 40216), (40223, 40373),
            (40380, 40485), (40492, 40611), (40618, 40709), (40716, 40769), (40776, 40795), (40802, 40883), (40890, 41019),
            (41026, 41052), (41059, 41222), (41229, 41458), (41465, 41476), (41483, 41524), (41531, 41596), (41603, 41726),
            (41733, 41744), (41751, 42002), (42009, 42029), (42036, 42075), (42082, 42350), (42357, 42437), (42444, 42462),
            (42469, 42554), (42561, 42622), (42629, 42727), (42734, 42783), (42790, 42864), (42871, 42930), (42937, 43233),
            (43240, 43307), (43314, 43405), (43412, 43555), (43562, 43633), (43640, 43717), (43724, 43977), (43984, 44034),
            (44041, 44147), (44154, 44183), (44190, 44219), (44226, 44246), (44253, 44364), (44371, 44440), (44447, 44482),
            (44489, 44541), (44548, 44709), (44716, 44747), (44754, 44817), (44824, 44887), (44894, 44970), (44977, 45005),
            (45012, 45048), (45055, 45106), (45113, 45437), (45444, 45546), (45553, 45623), (45630, 45660), (45667, 45708),
            (45715, 45749), (45756, 46000), (46007, 46024), (46031, 46139), (46146, 46180), (46187, 46306), (46313, 46415),
            (46422, 46436), (46443, 46481), (46488, 46518), (46525, 46578), (46585, 46631), (46638, 46770), (46777, 46801),
            (46808, 46826), (46833, 46932), (46939, 47048), (47055, 47069), (47076, 47140), (47147, 47594), (47601, 47629),
            (47636, 47697), (47704, 47789), (47796, 47886), (47893, 47906), (47913, 47979), (47986, 48003), (48010, 48120),
            (48127, 48173), (48180, 48235), (48242, 48372), (48379, 48437), (48444, 48610), (48617, 48755), (48762, 48800),
            (48807, 48833)]


def test():
    # Open the trace with Qtrace-DB
    dbm = DatabaseManager(f'sqlite:///{DATABASE_FILE}')
    trace = dbm.get_trace("x86_64")
    start, stop = TARGETS[1]
    first_inst = trace.get_instr(start)

    # Perform symbolic execution of the instructions
    symexec = QtraceSymExec(trace, Mode.PARAM_SYMBOLIC)
    symexec.initialize_register('rip', first_inst.RIP)
    symexec.initialize_register('rsp', first_inst.RSP)
    symexec.process_instr_sequence(start, stop)
    rax = symexec.get_register_ast("rax")

    # Load lookup tables
    ltms = [LookupTableLevelDB.load(TABLE_DIR)]

    # Perform Synthesis of the expression
    synthesizer = TopDownSynthesizer(ltms)
    synt_rax, simp = synthesizer.synthesize(rax)

    # Print synthesis results
    print(f"simplified: {simp}")
    print(f"synthesized expression: {synt_rax.pp_str}")
    print(f"size: {rax.node_count} -> {synt_rax.node_count} scale reduction:{synt_rax.node_count/rax.node_count:.2f}")

    trace.close()
    dbm.close()
    return symexec


if __name__ == "__main__":
    sx = test()
