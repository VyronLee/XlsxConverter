package.path = package.path .. ";../../output/?.lua"

local actor_conf_path = "ActorConf_Properties"
local equipment_conf_path = "EquipmentConf_Properties"

local actor_conf = require(actor_conf_path)
local equipment_conf = require(equipment_conf_path)

local all_actor_conf = actor_conf:getData()
print("Dump ActorConf.Properties: ")
print(all_actor_conf)

for i=1, 4 do
    print("Query record with 'id': " .. i)
    print(actor_conf:getData("id", i)[1])
end

local all_equipment_conf = equipment_conf:getData()
print("Dump EquipmentConf.Properties: ")
print(all_equipment_conf)

for i=1, 4 do
    print(("Query record with 'id': %s and 'quality': 1"):format(i))
    print(equipment_conf:getData("id", i, "quality", 1)[1])
end

print("Query record with 'quality': 1")
print(equipment_conf:getData("quality", 1))
