#include <SymphonyInterface.h>
int main() {
    SymEnvironment env;
    sym_open_environment(&env);
    sym_parse_command_line(&env, argc, argv);
    sym_load_problem(&env, "stein27.mps");
    sym_solve(&env);
    double obj_value;
    sym_get_obj_val(&env, &obj_value);
    printf("Objective: %f\n", obj_value);
    sym_close_environment(&env);
    return 0;
}