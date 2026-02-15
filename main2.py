import aircraft, analyses #type: ignore


concept_4 = aircraft.aircraft(2.5*1.5, 670000)
concept_4.set_weights(110000, 500000)
concept_4.wing_geometry(94.403, 10, 47.5, 183.2, 9563.28, 3.5095, .12, 0, .3, 1)
concept_4.set_engine(0.578, 4, 16640, 97000)
concept_4.update_MTOW()


print(f"MTOW Concept 4={concept_4.get_MTOW()} lbs")
concept_4.set_flight_param(0.9, 40000, 0.85)

[CL, CD] = (concept_4.calculate_CL_CD())
print(f"L/D={float(CL/CD)}")

analysis = analyses.study(concept_4)

#analysis.thrust_required([0.7, 1], 40000)
#analysis.range_integration(-20)
analysis.fuel_sensitivity([0,1000000])

