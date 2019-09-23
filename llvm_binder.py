import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float, c_int64

def inject_built_in(module):
    built_in = 'define void @"printFloat"(float) #0 {  %2 = alloca float, align 4  store float %0, float* %2, align 4  %3 = load float, float* %2, align 4  %4 = fpext float %3 to double  %5 = call i64 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i63 0, i64 0), double %4)  ret void}define void @"printInt"(i64) #0 {  %2 = alloca i64, align 4  store i64 %0, i64* %2, align 4  %3 = load i64, i64* %2, align 4  %4 = call i64 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i64 %3)  ret void}define void @"printString"(i8*) #0 {  %2 = alloca i8*, align 8  store i8* %0, i8** %2, align 8  %3 = load i8*, i8** %2, align 8  %4 = call i64 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.2, i64 0, i64 0), i8* %3)  ret void}'
    string_declare = '''@.str = private unnamed_addr constant [4 x i8] c"%f\\0A\\00", align 1@.str.1 = private unnamed_addr constant [4 x i8] c"%d\\0A\\00", align 1@.str.2 = private unnamed_addr constant [4 x i8] c"%s\\0A\\00", align 1'''
    strings = break_run(str(module))
    return string_declare + strings[0] + built_in + strings[1]


def break_run(module_string):
    module_string = module_string.replace('declare void @"printFloat"(float %".1")', "")
    module_string = module_string.replace('declare void @"printInt"(i64 %".1")', "")
    module_string = module_string.replace('declare void @"printString"(i8* %".1")', "")

    index = module_string.index('define i64 @"main"()')
    results = [module_string[0:index], module_string[index:]]
    return results


def bind(module, *args, optimize = False):
    module = inject_built_in(module)

    llvm_ir_parsed = llvm.parse_assembly(str(module))
    if False:
        
        pmb = llvm.create_pass_manager_builder()
        pmb.opt_level = 3

        fpm = llvm.create_function_pass_manager(llvm_ir_parsed)
        pmb.populate(fpm)

        pm = llvm.create_module_pass_manager()
        pmb.populate(pm)
        a = pm.run(llvm_ir_parsed)
        

    
    if optimize:
        opt_manager = llvm.PassManagerBuilder()
        mod_manager = llvm.ModulePassManager()

        mod_manager.add_constant_merge_pass()
        mod_manager.add_dead_arg_elimination_pass()
        mod_manager.add_function_inlining_pass(225)
        mod_manager.add_global_dce_pass()
        mod_manager.add_global_optimizer_pass()
        mod_manager.add_ipsccp_pass()
        mod_manager.add_dead_code_elimination_pass()
        mod_manager.add_cfg_simplification_pass()   
        mod_manager.add_gvn_pass()
        mod_manager.add_instruction_combining_pass()
        mod_manager.add_licm_pass()
        mod_manager.add_sccp_pass()
        mod_manager.add_type_based_alias_analysis_pass()
        mod_manager.add_basic_alias_analysis_pass()

        mod_manager.run(llvm_ir_parsed)

    ####################################################################

    llvm_ir_parsed.verify()


    # JIT
    target_machine = llvm.Target.from_default_triple().create_target_machine()
    engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
    engine.finalize_object()

    entry = engine.get_function_address("main")

    cfunc = CFUNCTYPE(c_int64)(entry)
  
    result = cfunc()
    #print()
    #print("Programa main:: {}".format(result))
    return [llvm_ir_parsed, result] 
