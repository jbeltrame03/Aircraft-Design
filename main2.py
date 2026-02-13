import aircraft, analyses #type: ignore

concept_1 = aircraft.aircraft(2.5*1.5, 670000)

concept_1.set_weights(110000, 400000)
concept_1.wing_geometry(100, 5, 45, 180, 7850, 4.127, 0.1, 16277.6, 0.3, 1)
concept_1.vertical_stab_geometry(20, 10, 45, 20, 0.1, 532.37, 0.20, 2, 50, 0)
concept_1.vertical_stab_geometry(20, 10, 45, 20, 0.1, 532.37, 0.20, 3, 50, 0)
concept_1.update_MTOW()
concept_1.set_engine(0.66, 4, 3163, 20187)
concept_1.update_MTOW()

concept_4 = aircraft.aircraft(2.5*1.5, 670000)
concept_4.set_weights(110000, 400000)
concept_4.wing_geometry(140, 108.3, 47, 43.2, 2681.64, 43.2*43.2/2681.64, .12, 0, .3, 1)
concept_4.wing_geometry(50, 10, 45, 140, 2100, (140**2)/2100, .12, 0, .3, 2)
concept_4.set_engine(0.578, 4, 16640, 97000)
concept_4.update_MTOW()

'''


analysis = analyses.study(concept_1)
analysis.Sweep_CDo([0,60])
analysis.thrust_required([0.7, 1], 40000)'''

print(f"MTOW Concept 1={concept_1.get_MTOW()} lbs")

print(f"MTOW Concept 4={concept_4.get_MTOW()} lbs")
concept_4.set_flight_param(0.9, 40000, 0.85)
concept_1.set_flight_param(0.9, 40000, 0.85)

print(concept_4.calculate_CDo())
print(concept_1.calculate_CDo())

analysis = analyses.study(concept_4)

analysis.thrust_required([0.7, 1], 40000)


