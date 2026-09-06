# -*- coding: utf-8 -*-
EN = {
    "mek_start": {
        "title": "Osmium and First Machines", "subtitle": "Metallurgic infuser, steel and steel casing",
        "intro": ["Mekanism is the strictest of the three tech lines. Four tiers of everything: circuits, alloys, pipes, factories. No part is skipped, but each next one is exactly twice as good.", "Osmium, infuser, steel, casing. From there the branch unfolds on its own — into chemistry, reactors, armor that flies."],
        "quests": {
            "osmium": {"title": "Osmium", "text": ["A bluish metal that lies everywhere and is needed by everything. Casings, cables, first parts. Beside it — tin, lead, fluorite and uranium; leave the uranium alone for now."]},
            "infuser": {"title": "Metallurgic Infuser", "text": ["The first machine, and already alchemy: an item is infused with a substance — carbon, redstone, diamond, tin — and becomes another item. Steel, alloys, reinforced materials — all from here."]},
            "steel": {"title": "Steel", "text": ["Iron plus enriched carbon — a blank; blank in the furnace — an ingot. Its own steel, different from IE's, and in this pack they'll have to coexist."]},
            "casing": {"title": "Steel Casing", "text": ["Steel, osmium, glass. The shared part of every machine in the mod — from enrichment chamber to fusion reactor."], "rewards": ["Pass to all the mod's machines"]},
            "circuit": {"title": "Control Circuits", "text": ["Basic from osmium, advanced from infused alloy, elite from reinforced, ultimate from atomic. The circuit tier is the ceiling of what you can build."]},
            "alloys": {"title": "Alloys", "text": ["Infused, reinforced, atomic. Each a tier higher and chemistry harder."]},
            "cables": {"title": "Transmission", "text": ["Cable for energy, pipe for fluid, pressurized tube for gas, transporter for items, conductor for heat. Five kinds, five tiers, one logic."]},
            "sorter": {"title": "Logistical Sorting", "text": ["By item, by tag, by color. Diversion and restrictive transporters steer the flow."]},
            "energy": {"title": "Energy Storage", "text": ["The cube stores and converts between grids. The induction matrix is a battery the size of a house."]},
            "configurator": {"title": "Configurator", "text": ["Sides, rotation, draining, pickup. The card copies one machine's settings to another."]},
            "box": {"title": "Cardboard Box", "text": ["A machine into a box — with contents and settings. Moving in a minute."]},
        },
    },
    "mek_ore": {
        "title": "Ore Processing", "subtitle": "From doubling to fivefold yield",
        "intro": ["This chapter is why people install Mekanism. Each machine in the chain adds a multiplier: two, three, four, five. Five ingots from one piece of ore isn't convenience — it's a different economy."],
        "quests": {
            "enrichment": {"title": "Enrichment Chamber (×2)", "text": ["Ore into two crushed pieces, pieces into two ingots. Also — enriched substances for the infuser."]}, "rewards": ["Twofold ore processing"],
            "crusher_mek": {"title": "Crusher and Combiner", "text": ["The crusher — ingots back to dust; the combiner — dust and stone into ore. The cycle is closed."]},
            "purification": {"title": "Purification Chamber (×3)", "text": ["Ore and oxygen — three pieces. Oxygen comes from the separator splitting water; keep the hydrogen — the jetpack will want it."]}, 
            "injection": {"title": "Chemical Injection (×4)", "text": ["Ore and hydrogen chloride — four shards. Chlorine from brine, hydrogen from water, together in the chemical infuser. This is a plant now."]},
            "evaporation": {"title": "Thermal Evaporation Plant", "text": ["A tower in the sun boils water to brine, brine to salt. The source of chlorine, sulfuric acid and heavy water. Taller and hotter is faster."]},
            "dissolution": {"title": "Dissolution and Crystallization (×5)", "text": ["Dissolve in acid, wash, crystallize, crush, enrich. Four new machines and a lot of energy. Five ingots from one ore — the mod's ceiling, and it pays back in an evening."]}, 
            "factory": {"title": "Factories", "text": ["One machine, several lanes: three, five, seven, nine. The tier installer upgrades a standing factory without taking it apart."]},
            "miner": {"title": "Digital Miner", "text": ["Radius, heights, filter — and it digs only what you named, touching nothing else. With the stone generator it leaves solid rock behind; with silk touch it brings blocks whole."]},
            "upgrades": {"title": "Machine Upgrades", "text": ["Speed, energy efficiency, gas filter, muffling, chunk anchor. Speed eats energy — balance it."]},
            "sawmill": {"title": "Sawmill and More", "text": ["The sawmill takes items apart, the smelter melts cheaply, the formulaic assemblicator crafts by formula."]},
        },
    },
    "mek_power": {
        "title": "Power Generation", "subtitle": "From heat generator to steam turbine",
        "intro": [],
        "quests": {
            "heat_gen": {"title": "Heat Generator", "text": ["Coal or lava. Weak, but from minute one."]},
            "solar": {"title": "Solar Panels", "text": ["Regular — a little; advanced three-by-three — noticeably."]},
            "wind": {"title": "Wind Generator", "text": ["Higher is stronger. On a Terralith peak — the best passive of the early game."]},
            "bio": {"title": "Bio Generator", "text": ["Plants through the crusher — biofuel. The farm feeds the power plant."]},
            "gas_gen": {"title": "Gas-Burning Generator", "text": ["Ethylene is the mod's densest gas. Biofuel, water and substrate in the reaction chamber make it; the generator burns it. This pair feeds a base up to the reactor."], "rewards": ["Main mid-game power source"]},
            "boiler": {"title": "Thermal Boiler", "text": ["Water to steam from heaters or a reactor. Steam to the turbine."]},
            "turbine": {"title": "Steam Turbine", "text": ["A rotor in a tower, blades on the rotor, condensers on top. Built right, it puts out millions per tick — and sounds real."], "rewards": ["Industrial-scale energy"]},
            "induction": {"title": "Induction Matrix", "text": ["Cells set capacity, providers set speed. Upper tiers store numbers that don't fit in a head."]},
        },
    },
    "mek_nuclear": {
        "title": "Nuclear Power", "subtitle": "Uranium, fission reactor, waste and radiation",
        "intro": ["A fission reactor doesn't explode. It melts — slowly, with warning — and leaves land you can't walk on for weeks. That's not punishment for a mistake, it's the price of the pack's strongest source.", "Build it far away. Set up emergency shutdown before the first fuel load. And don't take the Geiger counter off your belt."],
        "quests": {
            "uranium": {"title": "Uranium", "text": ["Deep and rare. Ingot to yellowcake, yellowcake to fuel. Unprotected it warms your hands in the worst sense."]},
            "hazmat": {"title": "Hazmat Suit", "text": ["The suit lowers the dose, the Geiger counter shows background, the dosimeter how much you've taken. Don't approach a reactor without all three."]},
            "fuel": {"title": "Fuel Assemblies", "text": ["Cake, centrifuge, solar neutron activator — hexafluoride, then fissile fuel. The assembly goes into the reactor and quietly burns."]},
            "reactor": {"title": "Fission Reactor", "text": ["Casing, ports, assemblies, rods, coolant. You set the burn rate — and you answer if temperature crosses the limit. Wire the logic adapter to an emergency stop before you load the first assembly. That's not advice. It's the only rule."], "rewards": ["Gigawatt power — and constant risk"]},
            "waste": {"title": "Waste", "text": ["The barrel slowly decays waste; a full barrel is a release. Waste also processes into polonium and plutonium, and that's where it gets interesting."]},
            "fusion": {"title": "Fusion Reactor", "text": ["Deuterium and tritium from heavy water, a hohlraum with fuel, a laser that lights a star. Then it burns on its own, no waste and no fear."], "rewards": ["Top-tier clean energy"]},
            "sps": {"title": "Supercritical Phase Shifter", "text": ["Polonium into antimatter at a monstrous energy cost. Antimatter to the nucleosynthesizer, which makes what doesn't exist."], "rewards": ["The top of Mekanism's tech tree"]},
        },
    },
    "mek_qio": {
        "title": "QIO and Teleportation", "subtitle": "Quantum storage and instant travel",
        "intro": [],
        "quests": {
            "teleport_core": {"title": "Teleportation Core", "text": ["The shared part of everything that breaks distance."]},
            "teleporter": {"title": "Teleporter", "text": ["Two teleporters on one frequency — and between them there's no path, only a step. Across dimensions too. The portable one carries you to any fixed one."]},
            "entangloporter": {"title": "Quantum Entangloporter", "text": ["Energy, fluid, gas, items — between two points with no pipe. Reactor at the world's edge, turbine at home."]},
            "qio_array": {"title": "QIO Drive Array", "text": ["Base, hyper-dense, time-dilating, supermassive. The names are honest."]},
            "qio_dash": {"title": "QIO Dashboard", "text": ["A window into storage without a single cable. Portable — in your pocket."]}, "rewards": ["Wireless storage of any capacity"],
            "qio_io": {"title": "Import and Export", "text": ["Importer puts in, exporter takes out by filter, adapter gives a signal."]},
            "stabilizer": {"title": "Dimensional Stabilizer", "text": ["Holds chunks. An ultimate circuit — and your base never sleeps."]},
        },
    },
    "mek_gear": {
        "title": "MekaSuit", "subtitle": "Power armor, modules and the Meka-Tool",
        "intro": ["MekaSuit by itself is diamond with a battery. Modules decide everything: over thirty, and each turns the suit into something new — a diver, a pilot, a miner who needs no pickaxe."],
        "quests": {
            "scuba": {"title": "Breathing and Flight", "text": ["Mask and tank — water. Hydrogen jetpack — sky; in this pack it's worn in an accessory slot, chestplate stays on. Free runners cushion falls and run up slopes."]},
            "atomic_disassembler": {"title": "Atomic Disassembler", "text": ["Digs everything, cuts everything, takes a vein whole. The first tool after which a pickaxe looks like a stick."]},
            "robit": {"title": "Robit", "text": ["Picks up, smelts, crafts, follows. The charge pad is home."]},
            "mekasuit": {"title": "MekaSuit Set", "text": ["Atomic alloy, ultimate circuits, diamonds — four pieces. Empty for now."]},
            "modification": {"title": "Modification Station", "text": ["Modules go in and out. Levels stack."]},
            "modules_core": {"title": "Core Modules", "text": ["Capacity, solar recharge, charge distribution. Without them the suit is empty in a minute. Electrolytic breathing — infinite air underwater."]},
            "modules_move": {"title": "Movement", "text": ["The gravitational modulator — creative flight in survival. Hydraulics — jump, boosting — run, plus lava and ice underfoot."]},
            "modules_util": {"title": "Utility", "text": ["Night vision, magnet, stabilization, laser and radiation shielding, Geiger and feeding — in helmet and chest."]},
            "mekatool": {"title": "Meka-Tool", "text": ["A whole vein, fortune or silk, till, shear, teleport, strike. The last tool you'll make."], "rewards": ["The tech branch's final tool"]},
            "laser": {"title": "Lasers", "text": ["Cuts at range. The amplifier stores, the tractor beam gathers drops."]},
            "security": {"title": "Security", "text": ["Machines — for your own only."]},
        },
    },
}
# исправление: награды у пары заданий указаны на уровне главы по ошибке — переносим
for cid in ("mek_ore", "mek_qio"):
    ch = EN[cid]
    for qid in list(ch["quests"]):
        pass
EN["mek_ore"]["quests"]["enrichment"]["rewards"] = ["Twofold ore processing"]
EN["mek_ore"]["quests"]["purification"]["rewards"] = ["Threefold ore processing"]
EN["mek_ore"]["quests"]["injection"]["rewards"] = ["Fourfold ore processing"]
EN["mek_ore"]["quests"]["dissolution"]["rewards"] = ["Fivefold ore processing — the mod's ceiling"]
EN["mek_ore"]["quests"]["miner"]["rewards"] = ["Fully automatic mining"]
EN["mek_qio"]["quests"]["qio_dash"]["rewards"] = ["Wireless storage of any capacity"]
EN["mek_ore"].pop("rewards", None)
EN["mek_qio"].pop("rewards", None)
