// Jae Chung 7-13-99
// Example of a aimple and dull Agent that
// illustrates the use of OTcl linkages


#include <stdio.h>
#include <string.h>
#include "agent.h"


class MyAgent : public Agent {
public:
        MyAgent();
protected:
        int command(int argc, const char*const* argv);
private:
        int    my_var1;
        double my_var2;
        void   MyPrivFunc(void);
};


static class MyAgentClass : public TclClass {
public:
        MyAgentClass() : TclClass("Agent/MyAgentOtcl") {}
        TclObject* create(int, const char*const*) {
                return(new MyAgent());
        }
} class_my_agent;


MyAgent::MyAgent() : Agent(PT_UDP) {
       bind("my_var1_otcl", &my_var1);
       bind("my_var2_otcl", &my_var2);
}


int MyAgent::command(int argc, const char*const* argv) {
      if(argc == 2) {
           if(strcmp(argv[1], "call-my-priv-func") == 0) {
                  MyPrivFunc();
                  return(TCL_OK);
           }
      }
      return(Agent::command(argc, argv));
}


void MyAgent::MyPrivFunc(void) {
      Tcl& tcl = Tcl::instance();
      tcl.eval("puts \"Message From MyPrivFunc\"");
      tcl.evalf("puts \"     my_var1 = %d\"", my_var1);
      tcl.evalf("puts \"     my_var2 = %f\"", my_var2);
}

