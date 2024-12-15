use quote::ToTokens;
use syn::{ItemFn, Visibility};

pub struct RustFunction {
    pub name: String,
    pub path: String,
    pub signature: String,
    pub doc: String,
}

impl RustFunction {
    pub fn new(func: &ItemFn, path: String) -> Self {
        Self {
            name: func.sig.ident.to_string(),
            path,
            signature: Self::format_signature(func),
            doc: Self::extract_doc_comment(func),
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
        let vis = &func.vis;
        let name = &func.sig.ident;
        let inputs = &func.sig.inputs;
        let output = &func.sig.output;

        let args = inputs
            .iter()
            .map(|arg| arg.to_token_stream().to_string())
            .collect::<Vec<_>>()
            .join(", ");

        format!(
            "{} fn {}({}){}",
            vis.to_token_stream(),
            name,
            args,
            output.to_token_stream()
        )
    }
}
