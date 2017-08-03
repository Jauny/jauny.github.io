for i := len(spec.FliprUUIDs) - 1; i >= 0; i-- {

spec.FliprUUIDs = append(spec.FliprUUIDs[:i], spec.FliprUUIDs[i+1:]...)
