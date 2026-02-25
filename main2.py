import aircraft, analyses #type: ignore


concept_4 = aircraft.aircraft(2.5*1.5, 670000)
concept_4.set_weights(110000, 500000)
concept_4.wing_geometry(94.403, 10, 47.5, 183.2, 9563.28, 3.5095, .06, 0, .3, 1)
concept_4.set_engine(0.578, 3, 16640, 97000)
concept_4.update_MTOW()

concept_5 = aircraft.aircraft(2.5*1.5, 670000)
concept_5.set_weights(110000, 500000)
concept_5.wing_geometry(60, 5, 40, 180, 5850, 5.54, .1, 0, .3, 1)
concept_5.set_engine(0.578, 2, 3163, 20187)

concept_5.update_MTOW()

print(f"MTOW Concept 5={concept_5.get_MTOW()} lbs")
concept_5.set_flight_param(0.9, 40000, 0.95)

[CL, CD] = (concept_5.calculate_CL_CD())
print(f"L/D={CL/CD}")


analysis = analyses.study(concept_5)

analysis.thrust_required([0.7, 1], 40000)
#analysis.range_integration(-200)
#analysis.fuel_sensitivity([0,1000000])
analysis.drag_buildup([0.7, 1.0], 40000)
