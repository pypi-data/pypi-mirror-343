from enum import Enum

from List.configDict import locationType, itemType
from List.inventory import misc, magic, keyblade, ability, form
from List.location.graph import DefaultLogicGraph, RequirementEdge, chest, popup, item_bonus, stat_bonus, hybrid_bonus, \
    LocationGraphBuilder, START_NODE
from Module.itemPlacementRestriction import ItemPlacementHelpers


class NodeId(str, Enum):
    DisneyCastleCourtyard = "DC Courtyard"
    DisneyCastleCourtyardChests = "DC Courtyard Chests"
    Library = "Library"
    LibraryChests = "Library Chests"
    LibraryPopup = "Library Popup"
    MinnieEscort = "Minnie Escort"
    CornerstoneHill = "Cornerstone Hill"
    CornerstoneHillChests = "Cornerstone Hill Chests"
    Pier = "Pier"
    PierChests = "Pier Chests"
    Waterway = "Waterway"
    WaterwayChests = "Waterway Chests"
    WindowsPopup = "Windows Popup"
    BoatPete = "Boat Pete"
    FuturePete = "Future Pete"
    WisdomPopup = "Wisdom Popup"
    Marluxia = "AS Marluxia"
    DataMarluxia = "Data Marluxia"
    LingeringWill = "Lingering Will"


class CheckLocation(str, Enum):
    CourtyardMythrilShard = "DC Courtyard Mythril Shard"
    CourtyardStarRecipe = "DC Courtyard Star Recipe"
    CourtyardApBoost = "DC Courtyard AP Boost"
    CourtyardMythrilStone = "DC Courtyard Mythril Stone"
    CourtyardBlazingStone = "DC Courtyard Blazing Stone"
    CourtyardBlazingShard = "DC Courtyard Blazing Shard"
    CourtyardMythrilShard2 = "DC Courtyard Mythril Shard (2)"
    LibraryTornPages = "Library Torn Pages"
    DisneyCastleMap = "Disney Castle Map"
    MinnieEscort = "Minnie Escort"
    CornerstoneHillMap = "Cornerstone Hill Map"
    CornerstoneHillFrostShard = "Cornerstone Hill Frost Shard"
    PierMythrilShard = "Pier Mythril Shard"
    PierHiPotion = "Pier Hi-Potion"
    WaterwayMythrilStone = "Waterway Mythril Stone"
    WaterwayApBoost = "Waterway AP Boost"
    WaterwayFrostStone = "Waterway Frost Stone"
    WindowOfTimeMap = "Window of Time Map"
    BoatPete = "Boat Pete"
    FuturePete = "Future Pete"
    Monochrome = "Monochrome"
    WisdomForm = "Wisdom Form"
    MarluxiaBonus = "Marluxia Bonus"
    MarluxiaEternalBlossom = "Marluxia (AS) Eternal Blossom"
    DataMarluxiaLostIllusion = "Marluxia (Data) Lost Illusion"
    LingeringWillBonus = "Lingering Will Bonus"
    LingeringWillProofOfConnection = "Lingering Will Proof of Connection"
    LingeringWillManifestIllusion = "Lingering Will Manifest Illusion"

class DCLogicGraph(DefaultLogicGraph):
    def __init__(self,reverse_rando,keyblade_unlocks):
        DefaultLogicGraph.__init__(self,NodeId)
        keyblade_lambda = lambda inv : not keyblade_unlocks or ItemPlacementHelpers.need_dc_keyblade(inv)
        self.logic[NodeId.DisneyCastleCourtyard][NodeId.DisneyCastleCourtyardChests] = keyblade_lambda
        self.logic[NodeId.Library][NodeId.LibraryChests] = keyblade_lambda
        self.logic[NodeId.CornerstoneHill][NodeId.CornerstoneHillChests] = keyblade_lambda
        self.logic[NodeId.Pier][NodeId.PierChests] = keyblade_lambda
        self.logic[NodeId.Waterway][NodeId.WaterwayChests] = keyblade_lambda
        if not reverse_rando:
            self.logic[START_NODE][NodeId.DisneyCastleCourtyard] = ItemPlacementHelpers.dc1_check
            self.logic[NodeId.MinnieEscort][NodeId.CornerstoneHill] = ItemPlacementHelpers.dc2_check
        else:
            self.logic[START_NODE][NodeId.CornerstoneHill] = ItemPlacementHelpers.dc1_check
            self.logic[NodeId.Marluxia][NodeId.DisneyCastleCourtyard] = ItemPlacementHelpers.dc2_check

        self.logic[NodeId.WisdomPopup][NodeId.LingeringWill] = ItemPlacementHelpers.need_proof_connection
        

def make_graph(graph: LocationGraphBuilder):
    dc = locationType.DC
    dc_logic = DCLogicGraph(graph.reverse_rando,graph.keyblades_unlock_chests)
    graph.add_logic(dc_logic)

    courtyard_chests = graph.add_location(NodeId.DisneyCastleCourtyardChests, [
        chest(16, CheckLocation.CourtyardMythrilShard, dc),
        chest(17, CheckLocation.CourtyardStarRecipe, dc),
        chest(18, CheckLocation.CourtyardApBoost, dc),
        chest(92, CheckLocation.CourtyardMythrilStone, dc),
        chest(93, CheckLocation.CourtyardBlazingStone, dc),
        chest(247, CheckLocation.CourtyardBlazingShard, dc),
        chest(248, CheckLocation.CourtyardMythrilShard2, dc),
    ])
    courtyard = graph.add_location(NodeId.DisneyCastleCourtyard, [])
    library_chests = graph.add_location(NodeId.LibraryChests, [
        chest(91, CheckLocation.LibraryTornPages, dc, vanilla=misc.TornPages),
    ])
    library = graph.add_location(NodeId.Library, [])
    library_popup = graph.add_location(NodeId.LibraryPopup, [
        popup(332, CheckLocation.DisneyCastleMap, dc),
    ])
    minnie_escort = graph.add_location(NodeId.MinnieEscort, [
        hybrid_bonus(38, CheckLocation.MinnieEscort, dc, vanilla=ability.AutoSummon),
    ])
    cornerstone_hill_chests = graph.add_location(NodeId.CornerstoneHillChests, [
        chest(79, CheckLocation.CornerstoneHillMap, dc),
        chest(12, CheckLocation.CornerstoneHillFrostShard, dc),
    ])
    cornerstone_hill = graph.add_location(NodeId.CornerstoneHill, [])
    pier_chests = graph.add_location(NodeId.PierChests, [
        chest(81, CheckLocation.PierMythrilShard, dc),
        chest(82, CheckLocation.PierHiPotion, dc),
    ])
    pier = graph.add_location(NodeId.Pier, [])
    waterway_chests = graph.add_location(NodeId.WaterwayChests, [
        chest(83, CheckLocation.WaterwayMythrilStone, dc),
        chest(84, CheckLocation.WaterwayApBoost, dc),
        chest(85, CheckLocation.WaterwayFrostStone, dc),
    ])
    waterway = graph.add_location(NodeId.Waterway, [])
    windows_popup = graph.add_location(NodeId.WindowsPopup, [
        popup(368, CheckLocation.WindowOfTimeMap, dc),
    ])
    boat_pete = graph.add_location(NodeId.BoatPete, [
        item_bonus(16, CheckLocation.BoatPete, dc, vanilla=ability.DodgeSlash),
    ])
    future_pete = graph.add_location(NodeId.FuturePete, [
        hybrid_bonus(17, CheckLocation.FuturePete, dc, vanilla=magic.Reflect),
        popup(261, CheckLocation.Monochrome, dc, vanilla=keyblade.Monochrome),
    ])
    wisdom_popup = graph.add_location(NodeId.WisdomPopup, [
        popup(262, CheckLocation.WisdomForm, dc, vanilla=form.WisdomForm),
    ])
    marluxia = graph.add_location(NodeId.Marluxia, [
        stat_bonus(67, CheckLocation.MarluxiaBonus, [dc, locationType.AS]),
        popup(548, CheckLocation.MarluxiaEternalBlossom, [dc, locationType.AS]),
    ])
    data_marluxia = graph.add_location(NodeId.DataMarluxia, [
        popup(553, CheckLocation.DataMarluxiaLostIllusion, [dc, locationType.DataOrg]),
    ])
    lingering_will = graph.add_location(NodeId.LingeringWill, [
        stat_bonus(70, CheckLocation.LingeringWillBonus, [dc, locationType.LW],
                   invalid_checks=[itemType.PROOF_OF_CONNECTION]),
        popup(587, CheckLocation.LingeringWillProofOfConnection, [dc, locationType.LW],
              invalid_checks=[itemType.PROOF_OF_CONNECTION]),
        popup(591, CheckLocation.LingeringWillManifestIllusion, [dc, locationType.LW],
              invalid_checks=[itemType.PROOF_OF_CONNECTION]),
    ])

    graph.register_superboss(data_marluxia)
    graph.register_superboss(lingering_will)
    graph.register_last_story_boss(wisdom_popup)
    
    graph.add_edge(courtyard, courtyard_chests)
    graph.add_edge(library, library_chests)
    graph.add_edge(cornerstone_hill, cornerstone_hill_chests)
    graph.add_edge(pier, pier_chests)
    graph.add_edge(waterway, waterway_chests)

    if not graph.reverse_rando:
        graph.add_edge(START_NODE, courtyard)
        graph.add_edge(courtyard, library)
        graph.add_edge(library, library_popup)
        graph.add_edge(library_popup, minnie_escort)
        graph.add_edge(minnie_escort, cornerstone_hill)
        graph.add_edge(cornerstone_hill, pier)
        graph.add_edge(pier, waterway, RequirementEdge(battle=True))
        graph.add_edge(waterway, windows_popup, RequirementEdge(battle=True))
        graph.add_edge(windows_popup, boat_pete, RequirementEdge(battle=True))
        graph.add_edge(boat_pete, future_pete, RequirementEdge(battle=True))
        graph.add_edge(future_pete, wisdom_popup)
        graph.add_edge(wisdom_popup, marluxia, RequirementEdge(battle=True))
        graph.add_edge(marluxia, data_marluxia)
        graph.add_edge(wisdom_popup, lingering_will, RequirementEdge(battle=True))

        graph.register_first_boss(minnie_escort)
        graph.register_superboss(marluxia)
    else:
        graph.add_edge(START_NODE, cornerstone_hill)
        graph.add_edge(cornerstone_hill, pier)
        graph.add_edge(pier, waterway, RequirementEdge(battle=True))
        graph.add_edge(waterway, windows_popup, RequirementEdge(battle=True))
        graph.add_edge(windows_popup, boat_pete, RequirementEdge(battle=True))
        graph.add_edge(boat_pete, future_pete, RequirementEdge(battle=True))
        graph.add_edge(future_pete, marluxia, RequirementEdge(battle=True))
        graph.add_edge(marluxia, courtyard)
        graph.add_edge(courtyard, library)
        graph.add_edge(library, library_popup)
        graph.add_edge(library_popup, minnie_escort)
        graph.add_edge(minnie_escort, wisdom_popup)
        graph.add_edge(wisdom_popup, data_marluxia, RequirementEdge(battle=True))
        graph.add_edge(wisdom_popup, lingering_will,RequirementEdge(battle=True))
        graph.register_first_boss(future_pete)
