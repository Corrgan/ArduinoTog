import pcbnew, sys
b = pcbnew.LoadBoard(sys.argv[1])
b.BuildConnectivity()
f = pcbnew.ZONE_FILLER(b)
f.Fill(b.Zones())
b.Save(sys.argv[1])
print("gefüllt")
