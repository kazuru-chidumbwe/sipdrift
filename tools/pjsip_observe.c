/* pjsip_observe — parse a SIP message with PJSIP and emit JSON axes.
 * Usage: pjsip_observe <file.sip>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <pjlib.h>
#include <pjlib-util.h>
#include <pjsip.h>

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
        } else if (c >= 0x20) {
            out[j++] = (char)c;
        }
    }
    out[j] = '\0';
}

static void emit_fail(const char *detail)
{
    char esc[512];
    json_escape(detail, esc, sizeof(esc));
    printf("{\"stack_id\":\"pjsip-lab\",\"ok\":false,\"start_line\":null,"
           "\"status_code\":null,\"via\":null,\"cseq\":null,\"detail\":\"%s\"}\n",
           esc);
}

int main(int argc, char **argv)
{
    pj_status_t status;
    pj_caching_pool cp;
    pj_pool_t *pool;
    pjsip_endpoint *endpt = NULL;
    FILE *fp;
    char *buf = NULL;
    long flen;
    pjsip_msg *msg;
    pjsip_parser_err_report err_list;
    char start_esc[1024], via_esc[2048], cseq_esc[512], detail_esc[512];
    char start_buf[768];
    char via_buf[1024];
    char cseq_buf[256];
    const char *start = NULL;
    const char *via = NULL;
    const char *cseq = NULL;
    int status_code = -1;
    int ok = 0;
    char detail[256] = "pjsip-lab";

    if (argc != 2) {
        fprintf(stderr, "usage: %s <file.sip>\n", argv[0]);
        return 2;
    }

    status = pj_init();
    if (status != PJ_SUCCESS) {
        emit_fail("pj_init failed");
        return 1;
    }
    pj_log_set_level(0);
    status = pjlib_util_init();
    if (status != PJ_SUCCESS) {
        emit_fail("pjlib_util_init failed");
        return 1;
    }

    pj_caching_pool_init(&cp, &pj_pool_factory_default_policy, 0);
    pool = pj_pool_create(&cp.factory, "obs", 4096, 4096, NULL);
    status = pjsip_endpt_create(&cp.factory, "sipdrift", &endpt);
    if (status != PJ_SUCCESS) {
        emit_fail("pjsip_endpt_create failed");
        return 1;
    }

    fp = fopen(argv[1], "rb");
    if (!fp) {
        emit_fail("open failed");
        return 2;
    }
    if (fseek(fp, 0, SEEK_END) != 0) {
        fclose(fp);
        emit_fail("seek failed");
        return 2;
    }
    flen = ftell(fp);
    if (flen < 0 || flen > 8 * 1024 * 1024) {
        fclose(fp);
        emit_fail("bad size");
        return 2;
    }
    rewind(fp);
    buf = pj_pool_alloc(pool, (pj_size_t)flen + 1);
    if (fread(buf, 1, (size_t)flen, fp) != (size_t)flen) {
        fclose(fp);
        emit_fail("read failed");
        return 2;
    }
    buf[flen] = '\0';
    fclose(fp);

    pj_list_init(&err_list);
    msg = pjsip_parse_msg(pool, buf, (pj_size_t)flen, &err_list);
    if (!msg) {
        emit_fail("pjsip_parse_msg failed");
        pjsip_endpt_destroy(endpt);
        pj_caching_pool_destroy(&cp);
        pj_shutdown();
        return 1;
    }

    if (msg->type == PJSIP_REQUEST_MSG) {
        char uri_buf[512];
        int n = pjsip_uri_print(PJSIP_URI_IN_REQ_URI, msg->line.req.uri, uri_buf, sizeof(uri_buf));
        if (n > 0) {
            pj_ansi_snprintf(start_buf, sizeof(start_buf), "%.*s %.*s SIP/2.0",
                             (int)msg->line.req.method.name.slen, msg->line.req.method.name.ptr,
                             n, uri_buf);
        } else {
            pj_ansi_snprintf(start_buf, sizeof(start_buf), "%.*s SIP/2.0",
                             (int)msg->line.req.method.name.slen, msg->line.req.method.name.ptr);
        }
        start = start_buf;
        ok = 1;
        pj_ansi_snprintf(detail, sizeof(detail), "pjsip-lab request");
    } else if (msg->type == PJSIP_RESPONSE_MSG) {
        pj_ansi_snprintf(start_buf, sizeof(start_buf), "SIP/2.0 %d %.*s",
                         msg->line.status.code,
                         (int)msg->line.status.reason.slen, msg->line.status.reason.ptr);
        start = start_buf;
        status_code = msg->line.status.code;
        ok = 1;
        pj_ansi_snprintf(detail, sizeof(detail), "pjsip-lab status=%d", status_code);
    } else {
        pj_ansi_snprintf(detail, sizeof(detail), "unknown msg type");
        ok = 0;
    }

    {
        pjsip_via_hdr *vh = (pjsip_via_hdr *)pjsip_msg_find_hdr(msg, PJSIP_H_VIA, NULL);
        if (vh) {
            char *p = via_buf;
            int n = pjsip_hdr_print_on((pjsip_hdr *)vh, via_buf, sizeof(via_buf) - 1);
            if (n > 0) {
                via_buf[n] = '\0';
                /* strip "Via: " or "v: " */
                if (!pj_ansi_strnicmp(via_buf, "Via:", 4)) {
                    p = via_buf + 4;
                    while (*p == ' ' || *p == '\t') p++;
                    via = p;
                } else if (!pj_ansi_strnicmp(via_buf, "v:", 2)) {
                    p = via_buf + 2;
                    while (*p == ' ' || *p == '\t') p++;
                    via = p;
                } else {
                    via = via_buf;
                }
            }
        }
    }
    {
        pjsip_cseq_hdr *ch = (pjsip_cseq_hdr *)pjsip_msg_find_hdr(msg, PJSIP_H_CSEQ, NULL);
        if (ch) {
            int n = pjsip_hdr_print_on((pjsip_hdr *)ch, cseq_buf, sizeof(cseq_buf) - 1);
            if (n > 0) {
                char *p = cseq_buf;
                cseq_buf[n] = '\0';
                if (!pj_ansi_strnicmp(cseq_buf, "CSeq:", 5)) {
                    p = cseq_buf + 5;
                    while (*p == ' ' || *p == '\t') p++;
                }
                cseq = p;
            }
        }
    }

    json_escape(start, start_esc, sizeof(start_esc));
    json_escape(via, via_esc, sizeof(via_esc));
    json_escape(cseq, cseq_esc, sizeof(cseq_esc));
    json_escape(detail, detail_esc, sizeof(detail_esc));

    /* Destroy endpoint before printing so logs cannot trail the JSON line. */
    pjsip_endpt_destroy(endpt);
    endpt = NULL;

    printf("{\"stack_id\":\"pjsip-lab\",\"ok\":%s,", ok ? "true" : "false");
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

    if (endpt)
        pjsip_endpt_destroy(endpt);
    pj_pool_release(pool);
    pj_caching_pool_destroy(&cp);
    pj_shutdown();
    return ok ? 0 : 1;
}
