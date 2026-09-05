-- sipdrift Kamailio observe helper (Lua) — Kamailio 5.7 KSR API

local OBS_PATH = "/tmp/sipdrift-kamailio-obs.json"

local function json_escape(s)
  if s == nil then
    return ""
  end
  s = tostring(s)
  s = s:gsub("\\", "\\\\")
  s = s:gsub("\"", "\\\"")
  s = s:gsub("\r", "\\r")
  s = s:gsub("\n", "\\n")
  s = s:gsub("\t", "\\t")
  return s
end

local function qstr(s)
  if s == nil or s == "" then
    return "null"
  end
  return string.format('"%s"', json_escape(s))
end

local function write_obs(payload)
  local f = io.open(OBS_PATH, "w")
  if not f then
    return
  end
  f:write(payload)
  f:write("\n")
  f:close()
end

function ksr_request_route()
  local method = KSR.pv.get("$rm") or ""
  local ruri = KSR.pv.get("$ru") or ""
  local via = KSR.pv.get("$hdr(Via)")
  local cseq = KSR.pv.get("$hdr(CSeq)")
  local start_line = string.format("%s %s SIP/2.0", method, ruri)
  local payload = string.format(
    '{"stack_id":"kamailio-lab","ok":true,"start_line":%s,"status_code":null,"via":%s,"cseq":%s,"detail":"kamailio-lab request"}',
    qstr(start_line), qstr(via), qstr(cseq)
  )
  write_obs(payload)
  KSR.sl.sl_send_reply(200, "OK")
  return 1
end

function ksr_reply_route()
  local code = KSR.pv.get("$rs")
  local reason = KSR.pv.get("$rr") or ""
  local via = KSR.pv.get("$hdr(Via)")
  local cseq = KSR.pv.get("$hdr(CSeq)")
  local status_code = tonumber(code)
  local start_line = string.format("SIP/2.0 %s %s", tostring(code or ""), reason)
  local sc = status_code and tostring(status_code) or "null"
  local payload = string.format(
    '{"stack_id":"kamailio-lab","ok":true,"start_line":%s,"status_code":%s,"via":%s,"cseq":%s,"detail":"kamailio-lab reply"}',
    qstr(start_line), sc, qstr(via), qstr(cseq)
  )
  write_obs(payload)
  return 1
end
