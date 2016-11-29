default_target: all

NINJA := ninja

NINJA_FLAGS :=
ifdef VERBOSE
NINJA_FLAGS += -v
endif
ifdef NP
NINJA_FLAGS += -j $(NP)
endif

TARGETS += all install test

$(TARGETS):
	$(NINJA) -C $(TOPDIR) $(NINJA_FLAGS) $(SUBDIR)/$@
clean:
	$(NINJA) -C $(TOPDIR) $(NINJA_FLAGS) -t clean $(SUBDIR)/all
