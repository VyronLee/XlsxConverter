------------------------------------------------------------
--      @file EquipmentConf.lua
--     @brief Auto generated by XlsxConverter, DONT EDIT IT!
--    @author VyronLee(lwz_jz@hotmail.com)
-- @Copyright Copyright(c) 2019, Apache-2.0
------------------------------------------------------------
local keys = {
	['id'] = {index=1,type="int",brief="装备ID"},
	['quality'] = {index=2,type="int",brief="装备品质"},
	['attack'] = {index=3,type="int",brief="附加攻击"},
	['defend'] = {index=4,type="int",brief="附加防御"},
}

local mt = {
	__index = function(t,k)
		return keys[k] and t[keys[k].index]
	end,
}
local __mt = setmetatable

local conf = {}

conf.data = {
	[1] = __mt({1,1,10,0,}, mt),
	[2] = __mt({2,1,10,0,}, mt),
	[3] = __mt({3,2,100,2,}, mt),
}

conf.indexes = {
	['id'] = {
		['1'] = {1},
		['2'] = {2},
		['3'] = {3},
	},
	['quality'] = {
		['1'] = {1,2},
		['2'] = {3},
	},
	['id-quality'] = {
		['1-1'] = {1},
		['2-1'] = {2},
		['3-2'] = {3},
	},
}

conf.parseArgs = function(self, ...)
	local keys, values = {}, {}
	local args = { ... }
	for idx,val in ipairs(args) do
		if idx % 2 == 1 then
			keys[#keys + 1] = val
		else
			values[#values + 1] = val
		end
	end
	return keys, values
end

conf.getData = function(self, ...)
	local keys, values = self:parseArgs(...)
	local keyHash = table.concat(keys, '-')
	local valueHash = table.concat(values, '-')
	local keyMap = self.indexes[keyHash] or {}
	local valueMap = keyMap[valueHash] or {}
	local ret  = {}
	for idx,val in ipairs(valueMap) do
		ret[#ret + 1] = self.data[val]
	end
	return ret
end

return conf