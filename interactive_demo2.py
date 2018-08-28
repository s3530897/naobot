import ro_to_xf_to_ro as ro
import time

def interact():
    while(True):
        result=ro.integration_testing()
        ro.str_sclassification(result)
        time.sleep(12)

if (
        __name__ == "__main__"):
    interact()