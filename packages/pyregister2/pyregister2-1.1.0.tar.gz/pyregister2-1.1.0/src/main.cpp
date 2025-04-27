#if defined(_WIN32) || defined(__CYGWIN__)
    #define BUILD_DLL
#endif

#include "pyregister.hpp"
#include <cstdint>
#include <vector>
#include <string>
#include <sstream>
#include <cstring>
#include <variant>
#include <cctype>
#include <iostream>

using Types = std::variant<uint8_t, uint16_t, uint32_t, uint64_t>;

// Concatena resultados numa string marcada
static std::string final_list(const std::vector<Types>& list, const std::vector<std::string>& order) {
    std::stringstream ss;
    for (size_t i = 0; i < list.size(); ++i) {
        ss << order[i] << "[:567:]";
        if (auto p = std::get_if<uint64_t>(&list[i]))      ss << *p;
        else if (auto p = std::get_if<uint32_t>(&list[i])) ss << *p;
        else if (auto p = std::get_if<uint16_t>(&list[i])) ss << *p;
        else if (auto p = std::get_if<uint8_t>(&list[i]))  ss << static_cast<uint32_t>(*p);
        ss << "[,013.,45gsd]";
    }
    return ss.str();
}

// Converte string para uppercase
static void to_uppercase(const char* in, char* out) {
    for (int i = 0; in[i]; ++i)
        out[i] = static_cast<char>(std::toupper(static_cast<unsigned char>(in[i])));
    out[std::strlen(in)] = '\0';
}

enum class OpKind {
    WriteAL, ReadAL, WriteAH, ReadAH,
    WriteBL, ReadBL, WriteBH, ReadBH,
    WriteCL, ReadCL, WriteCH, ReadCH,
    WriteDL, ReadDL, WriteDH, ReadDH,
    WriteAX, ReadAX, WriteBX, ReadBX,
    WriteCX, ReadCX, WriteDX, ReadDX,
    WriteEAX, ReadEAX, WriteEBX, ReadEBX,
    WriteECX, ReadECX, WriteEDX, ReadEDX,
    WriteRAX, ReadRAX, WriteRBX, ReadRBX,
    WriteRCX, ReadRCX, WriteRDX, ReadRDX,
    SYSCALL
};

struct Operation {
    OpKind kind;
    Types value;
    Operation(OpKind k, Types v) : kind(k), value(v) {}
};

class RegisterBatch {
    std::vector<Operation> ops;
public:
    void syscall(uint8_t v){ ops.emplace_back(OpKind::SYSCALL, (uint8_t)0); }

    // 8-bit
    void write_al(uint8_t v){ ops.emplace_back(OpKind::WriteAL, v); }  void read_al() { ops.emplace_back(OpKind::ReadAL,  (uint8_t)0); }
    void write_ah(uint8_t v){ ops.emplace_back(OpKind::WriteAH, v); }  void read_ah() { ops.emplace_back(OpKind::ReadAH,  (uint8_t)0); }
    void write_bl(uint8_t v){ ops.emplace_back(OpKind::WriteBL, v); }  void read_bl() { ops.emplace_back(OpKind::ReadBL,  (uint8_t)0); }
    void write_bh(uint8_t v){ ops.emplace_back(OpKind::WriteBH, v); }  void read_bh() { ops.emplace_back(OpKind::ReadBH,  (uint8_t)0); }
    void write_cl(uint8_t v){ ops.emplace_back(OpKind::WriteCL, v); }  void read_cl() { ops.emplace_back(OpKind::ReadCL,  (uint8_t)0); }
    void write_ch(uint8_t v){ ops.emplace_back(OpKind::WriteCH, v); }  void read_ch() { ops.emplace_back(OpKind::ReadCH,  (uint8_t)0); }
    void write_dl(uint8_t v){ ops.emplace_back(OpKind::WriteDL, v); }  void read_dl() { ops.emplace_back(OpKind::ReadDL,  (uint8_t)0); }
    void write_dh(uint8_t v){ ops.emplace_back(OpKind::WriteDH, v); }  void read_dh() { ops.emplace_back(OpKind::ReadDH,  (uint8_t)0); }
    // 16-bit
    void write_ax(uint16_t v){ ops.emplace_back(OpKind::WriteAX, v); } void read_ax() { ops.emplace_back(OpKind::ReadAX,  (uint16_t)0); }
    void write_bx(uint16_t v){ ops.emplace_back(OpKind::WriteBX, v); } void read_bx() { ops.emplace_back(OpKind::ReadBX,  (uint16_t)0); }
    void write_cx(uint16_t v){ ops.emplace_back(OpKind::WriteCX, v); } void read_cx() { ops.emplace_back(OpKind::ReadCX,  (uint16_t)0); }
    void write_dx(uint16_t v){ ops.emplace_back(OpKind::WriteDX, v); } void read_dx() { ops.emplace_back(OpKind::ReadDX,  (uint16_t)0); }
    // 32-bit
    #if defined(__i386) || defined(_M_IX86)
    void write_eax(uint32_t v){ ops.emplace_back(OpKind::WriteEAX, v); } void read_eax() { ops.emplace_back(OpKind::ReadEAX,  (uint32_t)0); }
    void write_ebx(uint32_t v){ ops.emplace_back(OpKind::WriteEBX, v); } void read_ebx() { ops.emplace_back(OpKind::ReadEBX,  (uint32_t)0); }
    void write_ecx(uint32_t v){ ops.emplace_back(OpKind::WriteECX, v); } void read_ecx() { ops.emplace_back(OpKind::ReadECX,  (uint32_t)0); }
    void write_edx(uint32_t v){ ops.emplace_back(OpKind::WriteEDX, v); } void read_edx() { ops.emplace_back(OpKind::ReadEDX,  (uint32_t)0); }
    // 64-bit
    #elif defined(__x86_64__) || defined(_M_X64) || defined(__ppc64__)
    void write_rax(uint64_t v){ ops.emplace_back(OpKind::WriteRAX, v); } void read_rax() { ops.emplace_back(OpKind::ReadRAX,  (uint64_t)0); }
    void write_rbx(uint64_t v){ ops.emplace_back(OpKind::WriteRBX, v); } void read_rbx() { ops.emplace_back(OpKind::ReadRBX,  (uint64_t)0); }
    void write_rcx(uint64_t v){ ops.emplace_back(OpKind::WriteRCX, v); } void read_rcx() { ops.emplace_back(OpKind::ReadRCX,  (uint64_t)0); }
    void write_rdx(uint64_t v){ ops.emplace_back(OpKind::WriteRDX, v); } void read_rdx() { ops.emplace_back(OpKind::ReadRDX,  (uint64_t)0); }

    void write_eax(uint32_t v){ ops.emplace_back(OpKind::WriteEAX, v); } void read_eax() { ops.emplace_back(OpKind::ReadEAX,  (uint32_t)0); }
    void write_ebx(uint32_t v){ ops.emplace_back(OpKind::WriteEBX, v); } void read_ebx() { ops.emplace_back(OpKind::ReadEBX,  (uint32_t)0); }
    void write_ecx(uint32_t v){ ops.emplace_back(OpKind::WriteECX, v); } void read_ecx() { ops.emplace_back(OpKind::ReadECX,  (uint32_t)0); }
    void write_edx(uint32_t v){ ops.emplace_back(OpKind::WriteEDX, v); } void read_edx() { ops.emplace_back(OpKind::ReadEDX,  (uint32_t)0); }

    #endif

    std::pair<std::vector<Types>, std::vector<std::string>> execute() {
        std::vector<Types> results;
        std::vector<std::string> order;
        uint8_t  t8;
        uint16_t t16;
        uint32_t t32;
        uint64_t t64;
        // Zerar
        asm volatile("xorl %%eax,%%eax" ::: "eax");
        asm volatile("xorl %%ebx,%%ebx" ::: "ebx");
        asm volatile("xorl %%ecx,%%ecx" ::: "ecx");
        asm volatile("xorl %%edx,%%edx" ::: "edx");

        asm volatile("xorq %%rax,%%rax" ::: "rax");
        asm volatile("xorq %%rbx,%%rbx" ::: "rbx");
        asm volatile("xorq %%rcx,%%rcx" ::: "rcx");
        asm volatile("xorq %%rdx,%%rdx" ::: "rdx");

        for (auto &op : ops) switch (op.kind) {
            case OpKind::SYSCALL: asm volatile("syscall" :::); break;

            case OpKind::WriteAL: asm volatile("movb %0,%%al" :: "r"(std::get<uint8_t>(op.value)) : "al"); break;
            case OpKind::ReadAL:  asm volatile("movb %%al,%0" : "=r"(t8) : : ); results.push_back(t8); order.push_back("AL"); break;
            case OpKind::WriteAH: asm volatile("movb %0,%%ah" :: "r"(std::get<uint8_t>(op.value)) : "ah"); break;
            case OpKind::ReadAH:  asm volatile("movb %%ah,%0" : "=r"(t8) : : ); results.push_back(t8); order.push_back("AH"); break;
            case OpKind::WriteBL: asm volatile("movb %0,%%bl" :: "r"(std::get<uint8_t>(op.value)) : "bl"); break;
            case OpKind::ReadBL:  asm volatile("movb %%bl,%0" : "=r"(t8) : : ); results.push_back(t8); order.push_back("BL"); break;
            case OpKind::WriteBH: asm volatile("movb %0,%%bh" :: "r"(std::get<uint8_t>(op.value)) : "bh"); break;
            case OpKind::ReadBH:  asm volatile("movb %%bh,%0" : "=r"(t8) : : ); results.push_back(t8); order.push_back("BH"); break;
            case OpKind::WriteCL: asm volatile("movb %0,%%cl" :: "r"(std::get<uint8_t>(op.value)) : "cl"); break;
            case OpKind::ReadCL:  asm volatile("movb %%cl,%0" : "=r"(t8) : : ); results.push_back(t8); order.push_back("CL"); break;
            case OpKind::WriteCH: asm volatile("movb %0,%%ch" :: "r"(std::get<uint8_t>(op.value)) : "ch"); break;
            case OpKind::ReadCH:  asm volatile("movb %%ch,%0" : "=r"(t8) : : ); results.push_back(t8); order.push_back("CH"); break;
            case OpKind::WriteDL: asm volatile("movb %0,%%dl" :: "r"(std::get<uint8_t>(op.value)) : "dl"); break;
            case OpKind::ReadDL:  asm volatile("movb %%dl,%0" : "=r"(t8) : : ); results.push_back(t8); order.push_back("DL"); break;
            case OpKind::WriteDH: asm volatile("movb %0,%%dh" :: "r"(std::get<uint8_t>(op.value)) : "dh"); break;
            case OpKind::ReadDH:  asm volatile("movb %%dh,%0" : "=r"(t8) : : ); results.push_back(t8); order.push_back("DH"); break;
            case OpKind::WriteAX: asm volatile("movw %0,%%ax" :: "r"(std::get<uint16_t>(op.value)) : "ax"); break;
            case OpKind::ReadAX:  asm volatile("movw %%ax,%0" : "=r"(t16) : : ); results.push_back(t16); order.push_back("AX"); break;
            case OpKind::WriteBX: asm volatile("movw %0,%%bx" :: "r"(std::get<uint16_t>(op.value)) : "bx"); break;
            case OpKind::ReadBX:  asm volatile("movw %%bx,%0" : "=r"(t16) : : ); results.push_back(t16); order.push_back("BX"); break;
            case OpKind::WriteCX: asm volatile("movw %0,%%cx" :: "r"(std::get<uint16_t>(op.value)) : "cx"); break;
            case OpKind::ReadCX:  asm volatile("movw %%cx,%0" : "=r"(t16) : : ); results.push_back(t16); order.push_back("CX"); break;
            case OpKind::WriteDX: asm volatile("movw %0,%%dx" :: "r"(std::get<uint16_t>(op.value)) : "dx"); break;
            case OpKind::ReadDX:  asm volatile("movw %%dx,%0" : "=r"(t16) : : ); results.push_back(t16); order.push_back("DX"); break;

            #if defined(__i386) || defined(_M_IX86)
            case OpKind::WriteEAX: asm volatile("movl %0,%%eax" :: "r"(std::get<uint32_t>(op.value)) : "eax"); break;
            case OpKind::ReadEAX:  asm volatile("movl %%eax,%0" : "=r"(t32) : : ); results.push_back(t32); order.push_back("EAX"); break;
            case OpKind::WriteEBX: asm volatile("movl %0,%%ebx" :: "r"(std::get<uint32_t>(op.value)) : "ebx"); break;
            case OpKind::ReadEBX:  asm volatile("movl %%ebx,%0" : "=r"(t32) : : ); results.push_back(t32); order.push_back("EBX"); break;
            case OpKind::WriteECX: asm volatile("movl %0,%%ecx" :: "r"(std::get<uint32_t>(op.value)) : "ecx"); break;
            case OpKind::ReadECX:  asm volatile("movl %%ecx,%0" : "=r"(t32) : : ); results.push_back(t32); order.push_back("ECX"); break;
            case OpKind::WriteEDX: asm volatile("movl %0,%%edx" :: "r"(std::get<uint32_t>(op.value)) : "edx"); break;
            case OpKind::ReadEDX:  asm volatile("movl %%edx,%0" : "=r"(t32) : : ); results.push_back(t32); order.push_back("EDX"); break;

            #elif defined(__x86_64__) || defined(_M_X64) || defined(__ppc64__)
            case OpKind::WriteEAX: asm volatile("movl %0,%%eax" :: "r"(std::get<uint32_t>(op.value)) : "eax"); break;
            case OpKind::ReadEAX:  asm volatile("movl %%eax,%0" : "=r"(t32) : : ); results.push_back(t32); order.push_back("EAX"); break;
            case OpKind::WriteEBX: asm volatile("movl %0,%%ebx" :: "r"(std::get<uint32_t>(op.value)) : "ebx"); break;
            case OpKind::ReadEBX:  asm volatile("movl %%ebx,%0" : "=r"(t32) : : ); results.push_back(t32); order.push_back("EBX"); break;
            case OpKind::WriteECX: asm volatile("movl %0,%%ecx" :: "r"(std::get<uint32_t>(op.value)) : "ecx"); break;
            case OpKind::ReadECX:  asm volatile("movl %%ecx,%0" : "=r"(t32) : : ); results.push_back(t32); order.push_back("ECX"); break;
            case OpKind::WriteEDX: asm volatile("movl %0,%%edx" :: "r"(std::get<uint32_t>(op.value)) : "edx"); break;
            case OpKind::ReadEDX:  asm volatile("movl %%edx,%0" : "=r"(t32) : : ); results.push_back(t32); order.push_back("EDX"); break;

            case OpKind::WriteRAX: asm volatile("movq %0,%%rax" :: "r"(std::get<uint64_t>(op.value)) : "rax"); break;
            case OpKind::ReadRAX:  asm volatile("movq %%rax,%0" : "=r"(t64) : : ); results.push_back(t64); order.push_back("RAX"); break;
            case OpKind::WriteRBX: asm volatile("movq %0,%%rbx" :: "r"(std::get<uint64_t>(op.value)) : "rbx"); break;
            case OpKind::ReadRBX:  asm volatile("movq %%rbx,%0" : "=r"(t64) : : ); results.push_back(t64); order.push_back("RBX"); break;
            case OpKind::WriteRCX: asm volatile("movq %0,%%rcx" :: "r"(std::get<uint64_t>(op.value)) : "rcx"); break;
            case OpKind::ReadRCX:  asm volatile("movq %%rcx,%0" : "=r"(t64) : : ); results.push_back(t64); order.push_back("RCX"); break;
            case OpKind::WriteRDX: asm volatile("movq %0,%%rdx" :: "r"(std::get<uint64_t>(op.value)) : "rdx"); break;
            case OpKind::ReadRDX:  asm volatile("movq %%rdx,%0" : "=r"(t64) : : ); results.push_back(t64); order.push_back("RDX"); break;
            #endif
        }
        ops.clear();
        return {results, order};
    }
};

extern "C" {
    static RegisterBatch global_batch;

    API_EXPORT void write_register(const char* reg, int v) {
        char up[5]; to_uppercase(reg, up);
        #define W(r,f) if(!strcmp(up,r)) return global_batch.write_##f(v)
        W("AL",al); W("AH",ah); W("BL",bl); W("BH",bh); W("CL",cl); W("CH",ch); W("DL",dl); W("DH",dh);
        W("AX",ax); W("BX",bx); W("CX",cx); W("DX",dx);

        #if defined(__i386) || defined(_M_IX86)    
        W("EAX",eax); W("EBX",ebx); W("ECX",ecx); W("EDX",edx);

        #elif defined(__x86_64__) || defined(_M_X64) || defined(__ppc64__)
        W("EAX",eax); W("EBX",ebx); W("ECX",ecx); W("EDX",edx);

        W("RAX",rax); W("RBX",rbx); W("RCX",rcx); W("RDX",rdx);

        #endif

        #undef W
    }

    API_EXPORT void read_register(const char* reg) {
        char up[5]; to_uppercase(reg, up);
        #define R(r,f) if(!strcmp(up,r)) return global_batch.read_##f()
        R("AL",al); R("AH",ah); R("BL",bl); R("BH",bh); R("CL",cl); R("CH",ch); R("DL",dl); R("DH",dh);
        R("AX",ax); R("BX",bx); R("CX",cx); R("DX",dx);

        #if defined(__i386) || defined(_M_IX86)
        R("EAX",eax); R("EBX",ebx); R("ECX",ecx); R("EDX",edx);

        #elif defined(__x86_64__) || defined(_M_X64) || defined(__ppc64__)
        R("EAX",eax); R("EBX",ebx); R("ECX",ecx); R("EDX",edx);

        R("RAX",rax); R("RBX",rbx); R("RCX",rcx); R("RDX",rdx);

        #endif

        #undef R
    }

    API_EXPORT void syscall() {
        global_batch.syscall(0);
    }

    API_EXPORT const char* execute() {
        static std::string res;
        auto [vals, ord] = global_batch.execute();
        res = final_list(vals, ord);
        return res.c_str();
    }
}