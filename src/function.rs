use syn::{File, ItemFn, Visibility};

pub struct RustFunction {
    pub name: String,
    pub path: String,
    pub signature: String,
    pub doc: String,
    pub source: String,
}

impl RustFunction {
    pub fn new(func: &ItemFn, path: String) -> Self {
        let mut func_clone = func.clone();
        // Keep the original attributes (like doc comments)
        func_clone.attrs = func.attrs.clone();

        let file = File {
            shebang: None,
            attrs: vec![],
            items: vec![syn::Item::Fn(func_clone)],
        };

        Self {
            name: func.sig.ident.to_string(),
            path,
            signature: Self::format_signature(func),
            doc: Self::extract_doc_comment(func),
            source: prettyplease::unparse(&file),
        }
    }

    pub fn is_public(func: &ItemFn, is_lib: bool) -> bool {
        matches!(func.vis, Visibility::Public(_))
            || (is_lib && matches!(func.vis, Visibility::Inherited))
    }

    fn extract_doc_comment(func: &ItemFn) -> String {
        func.attrs
            .iter()
            .filter(|attr| attr.path().is_ident("doc"))
            .filter_map(|attr| match &attr.meta {
                syn::Meta::NameValue(meta) => Some(&meta.value),
                _ => None,
            })
            .filter_map(|expr| match expr {
                syn::Expr::Lit(expr_lit) => Some(&expr_lit.lit),
                _ => None,
            })
            .filter_map(|lit| match lit {
                syn::Lit::Str(s) => Some(s.value().trim().to_string()),
                _ => None,
            })
            .collect::<Vec<_>>()
            .join("\n")
    }

    fn format_signature(func: &ItemFn) -> String {
        let mut func_sig = func.clone();
        func_sig.block = Box::new(syn::Block {
            brace_token: Default::default(),
            stmts: vec![],
        });

        let file = File {
            shebang: None,
            attrs: vec![],
            items: vec![syn::Item::Fn(func_sig)],
        };

        prettyplease::unparse(&file)
    }
}
