# -*- coding: utf-8 -*-
EN = {
    "space_ground": {
        "title": "Launch Table", "subtitle": "Steel, oxygen, fuel and the first rocket",
        "intro": [
            "Space in this pack starts not with stars but with a coal generator and a compressor. Ad Astra asks for exactly what real spaceflight asked for: metal, electricity and a great deal of patience.",
            "The path is single and strict: steel, plates, NASA workbench, rocket. Oxygen and fuel come separately, and without them a rocket is a monument.",
            "The mod's in-game guide is called Astrodux. Craft it first: same steps, but with pictures.",
        ],
        "quests": {
            "generator": {"title": "Coal Generator", "text": [
                "Six iron ingots, a coal block and a furnace. Twenty energy per tick from anything that burns — at the start there simply are no other sources.",
                "All Ad Astra machinery runs on its own energy, but the socket is shared with Create Addition and Mekanism: a cable will reach."]},
            "compressor": {"title": "Compressor", "text": [
                "Two pistons and six iron ingots. An ingot goes in, a plate comes out; a block goes in, nine plates come out.",
                "Plates go into everything, so the compressor sits beside the generator and never gets switched off."]},
            "furnace": {"title": "Etrionic Blast Furnace", "text": [
                "An upgraded blast furnace with two modes: smelting four times faster than usual and — the point — alloying.",
                "Iron plus coal in alloy mode gives steel. It's the mod's only steel recipe, and it's the bottleneck of the whole space program."]},
            "steel": {"title": "Steel", "text": [
                "A tier one rocket eats about ninety steel ingots. That's sixty-four pieces of iron and as much coal, run through the furnace one at a time.",
                "Automate the feed early — Create or Mekanism will handle it, and you'll save yourself an hour of clicking."]},
            "workbench": {"title": "NASA Workbench", "text": [
                "The table rockets are built on. Fourteen slots, each waiting for its part: nose cone, six steel blocks, four fins, two tanks and an engine."]},
            "oil": {"title": "Oil", "text": [
                "Oil wells gush in Earth's oceans — visible from far off. Oil doesn't regenerate, so pump extra.",
                "The fuel refinery converts oil to fuel one to one. Three buckets of fuel is one launch."]},
            "oxygen": {"title": "Oxygen", "text": [
                "Oxygen is extracted from water: a hundred millibuckets of water yield four of oxygen. The ratio is brutal, so run a pump or a Create pipe to the loader right away.",
                "Finished oxygen goes into tanks and fills your suit."]},
            "suit": {"title": "Space Suit", "text": [
                "Four pieces: helmet, suit, pants, boots. Only the full set works — three quarters of a suit saves nothing at all.",
                "The plain suit handles cold and lets you breathe. It won't handle Venus: that needs the netherite one."]},
            "rocket": {"title": "Tier One Rocket", "text": [
                "A nose cone with a lightning rod, six steel blocks, four fins, two tanks and a steel engine — all into the NASA workbench at once.",
                "A three-by-three launch pad, rocket in the center, fuel inside. Jump in the cockpit opens the planet map."],
                "rewards": ["A second pad — so you have something to come back on"]},
            "checklist": {"title": "Pre-flight Check", "text": [
                "The list that saves lives. Into the rocket's inventory: a second launch pad and three buckets of fuel for the return. On you: full tanks, food, weapons and — without fail — soul torches or glowstone.",
                "Ordinary torches break in vacuum, water evaporates, plants die. Forgetting the pad means staying on the Moon forever."],
                "tasks": ["A pad and return fuel are in the rocket"]},
        },
    },
    "space_moon": {
        "title": "The Moon", "subtitle": "First step, desh and life under a dome",
        "intro": ["Grey wasteland to the horizon, black sky and gravity six times weaker than home. There's nothing to breathe, water freezes in mid-air and torches go out — and here lies desh, without which you fly no further."],
        "quests": {
            "landing": {"title": "One Small Step", "text": [
                "The lander sets you down softly. Shift and right-click to take its contents, punch it to break the lander itself.",
                "First thing: look around and put the pad back down. It's your ticket home."]},
            "desh": {"title": "Desh", "text": [
                "Lunar ore sits at any depth, but is richest below zero. Desh goes into advanced machines, space stations and the tier two rocket.",
                "While you're at it, look for ice shards: they later become cryo fuel, three times more economical than the ordinary kind."]},
            "cheese": {"title": "Cheese", "text": ["Yes, the Moon has cheese ore. No, it isn't a mod joke — it's the mod's one joke, seen through to the end."]},
            "solar": {"title": "Solar Panel", "text": [
                "The sun shines brighter on the Moon than on Earth and the panel gives more. This is where the lunar grid begins.",
                "Cables run through special ducts: a plain cable in a wall breaks the seal."]},
            "distributor": {"title": "Oxygen Distributor", "text": [
                "The heart of any base off Earth. In a fully sealed room it creates a liveable zone and evens out the temperature too.",
                "The limit is six thousand blocks. The 'show' button highlights the volume and finds holes: one gap and everything blows out in a vortex.",
                "A water pump over an infinite source feeds it forever."]},
            "gravity": {"title": "Gravity Normalizer", "text": ["From zero to two g inside a sealed volume. Walking your base at a normal pace is a small luxury that costs energy."]},
            "rover": {"title": "Rover", "text": [
                "Two seats, sixteen slots and a radio that picks up real internet stations. Runs on the same fuel as rockets.",
                "It runs over mobs. On the Moon that's occasionally the only argument."]},
            "gadgets": {"title": "Instruments", "text": [
                "The TI-69 shows oxygen, temperature and gravity where you stand. The zip gun pushes you with a jet of oxygen — in orbital weightlessness it's the only way to move."]},
            "orbit": {"title": "Orbit", "text": [
                "A space station isn't crafted: you order it right on the planet map if the materials are in your inventory. Even Earth orbit asks for desh — so stations open only after the Moon.",
                "There's no air and no gravity in orbit. Without a zip gun you simply drift away."]},
            "tier2": {"title": "Tier Two Rocket", "text": [
                "Same layout, but tanks and engine are desh. The nose cone and fins stay steel at every tier.",
                "Next target: Mars."]},
        },
    },
    "space_mars": {
        "title": "Mars", "subtitle": "Ostrum, cryo fuel and a real colony",
        "intro": ["Red dust, minus sixty-five and canyons deeper than Earth's. Mars holds ostrum — the metal you make things from that survive Venus."],
        "quests": {
            "landing_mars": {"title": "Martian", "text": ["Colder than the Moon, and still no air. But there are temples, martian raptors and ore right in the canyon walls."]},
            "ostrum": {"title": "Ostrum", "text": ["Martian ore. Ostrum makes the cryo freezer, the energizer, pipes and, above all, the netherite space suit."]},
            "cryo": {"title": "Cryo Fuel", "text": [
                "The cryo freezer turns ice shards into cryo fuel: forty shards per bucket.",
                "A launch on it costs one bucket instead of three. A full rocket tank is three flights, and that's worth the fuss with ice."]},
            "energizer": {"title": "Energizer", "text": ["Two million energy in one block, and the charge survives being mined. Right-click an item to charge it."]},
            "netherite_suit": {"title": "Netherite Space Suit", "text": [
                "Ostrum plates over netherite armor and a large gas tank. Handles heat, grants permanent fire resistance and holds more oxygen.",
                "Without it Venus kills you in seconds. The mod has tested this."]},
            "tier3": {"title": "Tier Three Rocket", "text": ["Ostrum tanks and engine. Opens Venus and Mercury."]},
        },
    },
    "space_hot": {
        "title": "The Hot Planets", "subtitle": "Venus, Mercury and calorite",
        "intro": [
            "Four hundred sixty-four degrees, acid rain and leaden clouds. Venus is the most hostile place in the pack, and calorite lies exactly there.",
            "Mercury is simpler: a hundred sixty-seven degrees, not a drop of water and the brightest sun in the system — panels work there like nowhere else.",
        ],
        "quests": {
            "venus": {"title": "Planet of Storms", "text": [
                "Acid rain corrodes everything living, pygros attack in packs, sulfur creepers burst in a cloud of poison.",
                "You don't come here without the netherite suit. At all."]},
            "calorite": {"title": "Calorite", "text": ["Found on Venus and nowhere else. It makes the tier four rocket and the jet suit."]},
            "mercury": {"title": "Mercury", "text": [
                "The planet closest to the sun and the best place for solar panels in the whole pack. Iron is the only ore, but there's so much energy that a factory on Mercury pays for itself."]},
            "jet": {"title": "Jet Suit", "text": [
                "Calorite over the netherite suit, a calorite engine and an etrionic capacitor. It flies on energy: jump to rise, jump with sprint to accelerate.",
                "The mod's top armor and the most convenient way to cross any planet."]},
            "tier4": {"title": "Tier Four Rocket", "text": ["Calorite tanks and engine. The mod's last rocket — and the only one with the range for another star."]},
        },
    },
    "space_glacio": {
        "title": "Proxima Centauri", "subtitle": "Glacio — the end of the road and the start of a colony",
        "intro": [
            "Another star, another system. Glacio is the only Ad Astra world besides Earth with oxygen: minus twenty, snow, ice peaks and peaceful glacian rams.",
            "The mod's progression ends here. Beyond it is what you build yourself.",
        ],
        "quests": {
            "interstellar": {"title": "Interstellar", "text": ["You can take the suit off: the temperature is within range and there's air. After Venus it feels like a holiday."]},
            "glacio_life": {"title": "Life on Glacio", "text": ["Glacian rams give fur, ice goes to cryo fuel, and every ore appears here at once. The best place for a second base."]},
            "colony": {"title": "A Colony Off Earth", "text": [
                "A full base on another planet: oxygen distributor, pump, gravity normalizer, solar panels, airlocks and an energizer.",
                "Gather it all on one planet — and you never have to come home again."],
                "rewards": ["A second homeland, built with your own hands"]},
        },
    },
}
