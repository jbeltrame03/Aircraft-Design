import aircraft, analyses #type: ignore


concept_4 = aircraft.aircraft(2.5*1.5, 670000)
concept_4.set_weights(110000, 400000)
concept_4.wing_geometry(140, 108.3, 47, 43.2, 2681.64, 43.2*43.2/2681.64, .12, 0, .3, 1)
concept_4.wing_geometry(50, 10, 45, 140, 2100, (140**2)/2100, .12, 0, .3, 2)
concept_4.set_engine(0.578, 4, 16640, 97000)
concept_4.update_MTOW()


print(f"MTOW Concept 4={concept_4.get_MTOW()} lbs")
concept_4.set_flight_param(0.9, 40000, 0.85)

[CL, CD] = (concept_4.calculate_CL_CD())
print(CL/CD)

analysis = analyses.study(concept_4)

analysis.thrust_required([0.7, 1], 40000)


