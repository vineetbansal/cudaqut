# Directories
OUTPUT := _output
SLURM_DIR := Slurm
COMMAND := code

# Target Scripts
SLURM?=reconstruction_example.slurm 
DEBUG_LEVEL?=WARN
MAIN?=dist_run.py

# Misc
JNAME  := pytorch-dist
SLURM_PATH := $(SLURM_DIR)/$(SLURM)

# Colors 
BBlack='\033[1;30m'       # Black
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BYellow='\033[1;33m'      # Yellow
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BCyan='\033[1;36m'        # Cyan
BWhite='\033[1;37m'       # White
NC='\033[0m' # No Color

all: clean
	@mkdir -p $(OUTPUT)
	$(eval SB_ARGS := --job-name=$(JNAME))
	$(eval SLURM_JOB_ID := $(shell sbatch --parsable $(SB_ARGS) $(SLURM_PATH) $(MAIN) $(DEBUG_LEVEL)))
	@if [ -z "$(SLURM_JOB_ID)" ]; then \
			echo -e $(BRed) Failed to submit job. Exiting. $(NC); \
			exit 1; \
	fi
	$(eval FULL_OUTPUT := $(OUTPUT)/$(JNAME).$(SLURM_JOB_ID).out)
	@echo -e $(BBlue) Output file name: $(FULL_OUTPUT) $(NC)
	@echo -e $(BYellow) Waiting for Job to start... $(NC)
	@while [ ! -f "$(FULL_OUTPUT)" ]; do \
					sleep 1; \
	done
	@if command -v $(COMMAND) >/dev/null 2>&1; then \
					$(COMMAND) "$(FULL_OUTPUT)"; \
	else \
					echo -e $(BRed) Visual Studio Code not found. Output file is at: $(FULL_OUTPUT) $(NC); \
	fi
	@echo -e $(BYellow) Job Started. Opening Output file now. $(NC)
	@echo -e $(BBlue) Build Script Done! $(NC)

clean:
	@rm -rf $(OUTPUT)

.PHONY: all clean# Directories
OUTPUT := _output
SLURM_DIR := slurm
