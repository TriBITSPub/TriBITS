default_target: all

NINJA := ninja

NINJA_FLAGS :=
ifdef VERBOSE
NINJA_FLAGS += -v
endif
ifdef NP
NINJA_FLAGS += -j $(NP)
endif

all install test $(TARGETS):
	$(NINJA) -C $(TOPDIR) $(NINJA_FLAGS) $(SUBDIR)/$@
clean:
	$(NINJA) -C $(TOPDIR) $(NINJA_FLAGS) -t clean $(SUBDIR)/all
help:
	@echo "This Makefile supports the following standard targets:"
	@echo ""
	@for t in "all (default)" clean help install test; do echo "  $$t"; done
	@echo ""
	@echo "and the following project targets:"
	@echo ""
	@for t in $(sort $(TARGETS)); do echo "  $$t"; done
