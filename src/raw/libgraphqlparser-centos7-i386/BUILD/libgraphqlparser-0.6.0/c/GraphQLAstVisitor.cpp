/**
 * Copyright (c) 2015, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

#include "c/GraphQLAstVisitor.h"
#include "AstVisitor.h"

using namespace facebook::graphql::ast;

#include "c/GraphQLAstForEachConcreteType.h"

#define DECLARE_VISIT(type, snake_type) \
  bool visit##type(const type &node) override; \
  void endVisit##type(const type &node) override;

class CVisitorBridge : public visitor::AstVisitor {
  const struct GraphQLAstVisitorCallbacks *callbacks_;
  void *userData_;
public:
  explicit CVisitorBridge(const struct GraphQLAstVisitorCallbacks *callbacks,
                          void *userData)
    : callbacks_(callbacks), userData_(userData) {}

  ~CVisitorBridge() {}

  FOR_EACH_CONCRETE_TYPE(DECLARE_VISIT)
};

#define IMPLEMENT_VISIT(type, snake_type)                                \
  bool CVisitorBridge::visit##type(const type &node) {                  \
    if (callbacks_->visit_##snake_type) {                               \
      return callbacks_->visit_##snake_type(                            \
        (const struct GraphQLAst##type *)&node, userData_);             \
    }                                                                   \
    return true;                                                        \
  }                                                                     \
  void CVisitorBridge::endVisit##type(const type &node) {               \
    if (callbacks_->end_visit_##snake_type) {                           \
      callbacks_->end_visit_##snake_type(                               \
        (const struct GraphQLAst##type *)&node, userData_);             \
    }                                                                   \
  }

FOR_EACH_CONCRETE_TYPE(IMPLEMENT_VISIT)

void graphql_node_visit(struct GraphQLAstNode *node,
                        const struct GraphQLAstVisitorCallbacks *callbacks,
                        void *userData)
{
  CVisitorBridge visitor(callbacks, userData);
  if (node) {
    ((facebook::graphql::ast::Node *)node)->accept(&visitor);
  }
}
