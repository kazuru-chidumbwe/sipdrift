# Build lab observe helpers (requires Sofia and/or PJSIP on the host).

SOFIA_CFLAGS := $(shell pkg-config --cflags sofia-sip-ua 2>/dev/null)
SOFIA_LIBS := $(shell pkg-config --libs sofia-sip-ua 2>/dev/null)

PJDIR ?= /opt/atlas/pjproject
-include $(PJDIR)/build.mak

.PHONY: all sofia pjsip clean

all: sofia

sofia: sofia_observe

sofia_observe: sofia_observe.c
	gcc -O2 -Wall -o $@ $< $(SOFIA_CFLAGS) $(SOFIA_LIBS)

pjsip: pjsip_observe

pjsip_observe: pjsip_observe.c
	gcc -O2 -Wall -o $@ $< $(APP_CFLAGS) -I$(PJDIR)/pjlib/include \
		-I$(PJDIR)/pjlib-util/include -I$(PJDIR)/pjnath/include \
		-I$(PJDIR)/pjmedia/include -I$(PJDIR)/pjsip/include \
		$(APP_LDFLAGS) $(APP_LDLIBS)

clean:
	rm -f sofia_observe pjsip_observe
