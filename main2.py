import aircraft, analyses #type: ignore


concept_4 = aircraft.aircraft(2.5*1.5, 670000)
concept_4.set_weights(110000, 500000)
concept_4.wing_geometry(94.403, 10, 47.5, 183.2, 9563.28, 3.5095, .06, 0, .3, 1)
concept_4.get_structure_weight()
concept_4.composites_struct(True)
concept_4.set_engine(0.578, 4, 16640, 97000)
concept_4.update_MTOW()


print(f"MTOW Concept 1 ={concept_4.get_MTOW()} lbs")
concept_4.set_flight_param(0.9, 40000, 0.95)

[CL, CD] = (concept_4.calculate_CL_CD())
print(f"L/D={CL/CD}")


analysis = analyses.study(concept_4)
analysis.drag_buildup([0.7, 1.0], 40000)
analysis.range_integration(-1000)


concept2 = aircraft.aircraft(2.5*1.5, 670000)
concept2.set_weights(110000, 500000)
concept2.wing_geometry(65.4, 5, 40, 220, 7742, 6.252, 0.1, 2*7742, 0.3, 1)
concept2.fuselage_geometry(150, 26.6, 8000, 2, 65.4, 5, 220, 40)
concept2.composites_struct(True)
concept2.update_MTOW()
concept2.set_flight_param(0.9, 40000, 0.95)
concept2.set_engine(0.578, 4, 16640, 97000)
concept2.update_MTOW()

print(f"MTOW Concept 2 ={concept2.get_MTOW()} lbs")

[CL, CD] = (concept2.calculate_CL_CD())
print(f"L/D={CL/CD}")
analysis = analyses.study(concept2)

analysis.drag_buildup([0.7, 1.0], 40000)
analysis.range_integration(-1000)
