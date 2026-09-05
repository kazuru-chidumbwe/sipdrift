/* sofia_observe — parse a SIP message with Sofia-SIP and emit JSON axes.
 *
 * Usage: sofia_observe <file.sip>
 * Stdout: one JSON object with stack_id, ok, start_line, status_code, via, cseq, detail
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include <sofia-sip/msg.h>
#include <sofia-sip/sip.h>
#include <sofia-sip/sip_header.h>
#include <sofia-sip/sip_protos.h>
#include <sofia-sip/url.h>

static void json_escape(const char *in, char *out, size_t outsz)
{
  size_t j = 0;
  if (!in) {
    out[0] = '\0';
    return;
  }
  for (size_t i = 0; in[i] && j + 2 < outsz; i++) {
    unsigned char c = (unsigned char)in[i];
    if (c == '"' || c == '\\') {
      out[j++] = '\\';
      out[j++] = (char)c;
    } else if (c == '\n') {
      out[j++] = '\\';
      out[j++] = 'n';
    } else if (c == '\r') {
      out[j++] = '\\';
      out[j++] = 'r';
    } else if (c < 0x20) {
      /* skip other controls */
    } else {
      out[j++] = (char)c;
    }
  }
  out[j] = '\0';
}

static char *header_value(su_home_t *home, sip_header_t *h, const char *name)
{
  char *full;
  size_t nlen;
  if (!h)
    return NULL;
  full = sip_header_as_string(home, h);
  if (!full)
    return NULL;
  nlen = strlen(name);
  if (strncasecmp(full, name, nlen) == 0 && full[nlen] == ':') {
    char *p = full + nlen + 1;
    while (*p == ' ' || *p == '\t')
      p++;
    return p;
  }
  return full;
}

int main(int argc, char **argv)
{
  FILE *fp;
  char *buf = NULL;
  long flen;
  msg_t *msg;
  sip_t *sip;
  su_home_t home[1] = { SU_HOME_INIT(home) };
  char start_esc[1024], via_esc[2048], cseq_esc[512], detail_esc[512];
  const char *start = NULL;
  const char *via = NULL;
  const char *cseq = NULL;
  int status_code = -1;
  int ok = 0;
  char detail[256] = "";

  if (argc != 2) {
    fprintf(stderr, "usage: %s <file.sip>\n", argv[0]);
    return 2;
  }

  fp = fopen(argv[1], "rb");
  if (!fp) {
    perror(argv[1]);
    return 2;
  }
  if (fseek(fp, 0, SEEK_END) != 0) {
    fclose(fp);
    return 2;
  }
  flen = ftell(fp);
  if (flen < 0 || flen > 8 * 1024 * 1024) {
    fclose(fp);
    return 2;
  }
  rewind(fp);
  buf = malloc((size_t)flen + 1);
  if (!buf) {
    fclose(fp);
    return 2;
  }
  if (fread(buf, 1, (size_t)flen, fp) != (size_t)flen) {
    free(buf);
    fclose(fp);
    return 2;
  }
  buf[flen] = '\0';
  fclose(fp);

  msg = msg_make(sip_default_mclass(), 0, buf, flen);
  free(buf);
  if (!msg) {
    printf("{\"stack_id\":\"sofia-lab\",\"ok\":false,\"start_line\":null,"
           "\"status_code\":null,\"via\":null,\"cseq\":null,"
           "\"detail\":\"msg_make failed\"}\n");
    return 1;
  }

  sip = sip_object(msg);
  if (!sip) {
    msg_destroy(msg);
    printf("{\"stack_id\":\"sofia-lab\",\"ok\":false,\"start_line\":null,"
           "\"status_code\":null,\"via\":null,\"cseq\":null,"
           "\"detail\":\"sip_object null\"}\n");
    return 1;
  }

  if (sip->sip_request) {
    char line[768];
    char *uri = url_as_string(home, sip->sip_request->rq_url);
    snprintf(line, sizeof(line), "%s %s %s",
             sip->sip_request->rq_method_name ? sip->sip_request->rq_method_name : "UNKNOWN",
             uri ? uri : "",
             sip->sip_request->rq_version ? sip->sip_request->rq_version : "SIP/2.0");
    start = su_strdup(home, line);
    ok = 1;
    snprintf(detail, sizeof(detail), "sofia-lab request method=%s",
             sip->sip_request->rq_method_name ? sip->sip_request->rq_method_name : "?");
  } else if (sip->sip_status) {
    char line[768];
    snprintf(line, sizeof(line), "%s %d %s",
             sip->sip_status->st_version ? sip->sip_status->st_version : "SIP/2.0",
             sip->sip_status->st_status,
             sip->sip_status->st_phrase ? sip->sip_status->st_phrase : "");
    start = su_strdup(home, line);
    status_code = sip->sip_status->st_status;
    ok = 1;
    snprintf(detail, sizeof(detail), "sofia-lab status=%d", status_code);
  } else {
    snprintf(detail, sizeof(detail), "no request/status line (errors=%u complete=%d)",
             msg_extract_errors(msg), msg_is_complete(msg));
    ok = 0;
  }

  if (sip->sip_via) {
    via = header_value(home, (sip_header_t *)sip->sip_via, "Via");
  }
  if (sip->sip_cseq) {
    cseq = header_value(home, (sip_header_t *)sip->sip_cseq, "CSeq");
  }

  json_escape(start, start_esc, sizeof(start_esc));
  json_escape(via, via_esc, sizeof(via_esc));
  json_escape(cseq, cseq_esc, sizeof(cseq_esc));
  json_escape(detail, detail_esc, sizeof(detail_esc));

  printf("{\"stack_id\":\"sofia-lab\",\"ok\":%s,", ok ? "true" : "false");
  if (start)
    printf("\"start_line\":\"%s\",", start_esc);
  else
    printf("\"start_line\":null,");
  if (status_code >= 0)
    printf("\"status_code\":%d,", status_code);
  else
    printf("\"status_code\":null,");
  if (via)
    printf("\"via\":\"%s\",", via_esc);
  else
    printf("\"via\":null,");
  if (cseq)
    printf("\"cseq\":\"%s\",", cseq_esc);
  else
    printf("\"cseq\":null,");
  printf("\"detail\":\"%s\"}\n", detail_esc);

  msg_destroy(msg);
  su_home_deinit(home);
  return ok ? 0 : 1;
}
