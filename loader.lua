local function validate_license()
    local key = script_key or "INVALID"
    local hwid = game:GetService("RbxAnalyticsService"):GetClientId()
    
    local request_func = syn and syn.request or request or http_request or function() end
    if type(request_func) ~= "function" then
        game:Shutdown()
        return error("PARADOX: No request function found. Use a supported executor.")
    end
    
    local response = request_func({
        Url = "https://paradox-bot.onrender.com/validate",
        Method = "POST",
        Headers = {["Content-Type"] = "application/json"},
        Body = game:GetService("HttpService"):JSONEncode({key = key, hwid = hwid})
    })
    
    local data = game:GetService("HttpService"):JSONDecode(response.Body)
    
    if not data.valid then
        game:Shutdown()
        return error("PARADOX: Invalid key or HWID mismatch. Purchase a key to access.")
    end
    
    return true
end

validate_license()

local main_script = game:HttpGet("https://paradox-bot.onrender.com/paradox_core.lua")
loadstring(main_script)()
print("✅ PARADOX loaded successfully!")
