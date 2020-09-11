class CTopLevelWindowIterator
{
public:
    CTopLevelWindowIterator(DWORD dwProcessId);
    ~CTopLevelWindowIterator();

    HWND First();
    HWND Next();

protected:
    static BOOL CALLBACK EnumProc(HWND hwnd, LPARAM lp);

    BOOL OnEnumProc(HWND hwnd);

    struct
    {
        DWORD   dwProcessId;    // process id
        DWORD   dwNumAlloced;   // number of HWND array elements allocated
        DWORD   dwNumUsed;      // number of HWND array elements used
        DWORD   dwCurrIdx;      // HWND array current index
        HWND *  paHWND;         // pointer to the array of top level window handles
    } m;
};
