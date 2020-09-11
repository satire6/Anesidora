class CEnvBlock
{
public:
    CEnvBlock (const char * pszToken)
    {
        memset (&m, 0, sizeof (m));
        m.pszToken  = pszToken;
    }
    ~CEnvBlock (void)
    {
    }
    void    Create (const char *    pszEnvKeyToAddToChildProcessEnvBlock,
                    CString &       strEnvForChildProcess);
private:
    struct
    {
        const char *    pszToken;
    } m;
private:
    void    insert_env_block_key_value_pair    (CString &   strEnvForChildProcess,
                                                int *       pInsertIdx,
                                                char *      lpszVariable);
};
