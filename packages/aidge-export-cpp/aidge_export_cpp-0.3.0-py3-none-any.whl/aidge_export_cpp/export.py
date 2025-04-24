import aidge_core
from aidge_export_cpp import ExportLibCpp

def export(export_folder_name, graphview, scheduler, mem_wrapping=False):
    print("Warning: This function is deprecated, check tutorial https://eclipse.dev/aidge/source/Tutorial/export_cpp.html to find the new way to generate a C++ export.")
    aidge_core.export_utils.scheduler_export(
        scheduler,
        export_folder_name,
        ExportLibCpp,
        memory_manager=aidge_core.mem_info.generate_optimized_memory_info,
        memory_manager_args={
            "stats_folder": f"{export_folder_name}/stats",
            "wrapping": mem_wrapping
        }
    )
